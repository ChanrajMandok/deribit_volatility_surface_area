import os
import asyncio
import threading

from singleton_decorator import singleton
from deribit_arb_app.services import logger
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.enums.enum_volatility_index_currency import EnumVolatilityIndexCurrency
from deribit_arb_app.services.deribit_api.service_api_deribit_utils import ServiceApiDeribitUtils
from deribit_arb_app.schedulers.scheduler_instrument_refresh import SchedulerVsaInstrumentsRefresh
from deribit_arb_app.model.model_subscribable_volatility_index import ModelSubscribableVolatilityIndex
from deribit_arb_app.services.managers.service_implied_volatility_queue_manager import ServiceImpliedVolatilityQueueManager
from deribit_arb_app.services.managers.service_instruments_subscription_manager import ServiceInstrumentsSubscriptionManager
from deribit_arb_app.utils.utils_asyncio import (asyncio_create_task_log_exception, loop_run_forever_log_exception, loop_create_task_log_exception, get_or_create_eventloop)

    ########################################################################################################################
    # Service runs all tasks to construct Volatility Surface area -> Instument subscriptions, Observers and Asyncio Queues #
    ########################################################################################################################

@singleton
class ServiceImpliedVolatilitySurfaceAreaTaskManager():

    def __init__(self):
        self.instruments_queue = asyncio.Queue()
        self.implied_volatility_queue = asyncio.Queue()
        self.service_api_deribit_utils = ServiceApiDeribitUtils()
        self.minimum_liquidity_threshold = int(os.environ.get('VSA_MINIMUM_LIQUIDITY_THRESHOLD', None))
        self.service_implied_volatility_queue_manager = ServiceImpliedVolatilityQueueManager(self.implied_volatility_queue)
        self.scheduler_instrument_refresh = SchedulerVsaInstrumentsRefresh(implied_volatility_queue=self.implied_volatility_queue,
                                                                                                instruments_queue=self.instruments_queue)
        self.service_instruments_subscription_manager = ServiceInstrumentsSubscriptionManager(implied_volatility_queue=self.implied_volatility_queue,
                                                                                                                instruments_queue=self.instruments_queue)

    def create_producer(self, currency: str):
        inner_loop_thread = threading.Thread(target=lambda: self.run_scheduler(currency=currency), name='vsa_producer')
        inner_loop_thread.start()
        self.run_consumer()

    def run_scheduler(self, currency: str):
        thread_2_loop = get_or_create_eventloop()
        loop_run_forever_log_exception(loop=thread_2_loop, awaitable=self.build_vsa_tasks(currency=currency), logger=logger, origin=f"{self.__class__.__name__} Scheduler")

    def run_consumer(self):
        if threading.current_thread() != threading.main_thread():
            raise Exception(f"{self.__class__.__name__} consumer not on main thread")
        thread_main_loop = get_or_create_eventloop()
        loop_run_forever_log_exception(loop=thread_main_loop, awaitable=self.consume_vsa_tasks(), logger=logger, origin=f"{self.__class__.__name__} consumer")
        
    def get_index_and_volatility_index(self, currency: str) -> tuple[ModelSubscribableIndex, ModelSubscribableVolatilityIndex]:
        index_currency_value = getattr(EnumIndexCurrency, currency.upper()).value
        volatility_index_currency_value = getattr(EnumVolatilityIndexCurrency, currency.upper()).value
        index = ModelSubscribableIndex(name=index_currency_value)
        volatility_index = ModelSubscribableVolatilityIndex(name=volatility_index_currency_value)
        return index, volatility_index
        
    async def build_vsa_tasks(self, currency: str, kind="option",):
        index, volatility_index = self.get_index_and_volatility_index(currency=currency)
        self.scheduler_instrument_refresh.run(kind=kind,
                                              index=index,
                                              volatility_index = volatility_index,
                                              currency=currency,
                                              minimum_liquidity_threshold=self.minimum_liquidity_threshold
                                             )
        
    async def consume_vsa_tasks(self):
        awaitable = self.service_instruments_subscription_manager.manage_instruments_queue()
        asyncio_create_task_log_exception(awaitable=awaitable, logger=logger, origin=f"{self.__class__.__name__} consume_vsa_tasks")
        
