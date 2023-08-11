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
from deribit_arb_app.services.managers.service_implied_volatility_observer_manager import ServiceImpliedVolatilityObserverManager
from deribit_arb_app.utils.utils_asyncio import (asyncio_create_task_log_exception, loop_run_forever_log_exception, loop_create_task_log_exception)



    ########################################################################################################################
    # Service runs all tasks to construct Volatility Surface area -> Instument subscriptions, Observers and Asyncio Queues #
    ########################################################################################################################

@singleton
class ServiceImpliedVolatilitySurfaceAreaTaskManager():

    def __init__(self):
        self.implied_volatility_queue = asyncio.Queue()
        self.service_api_deribit_utils = ServiceApiDeribitUtils()
        self.minimum_liquidity_threshold = int(os.environ.get('VSA_MINIMUM_LIQUIDITY_THRESHOLD', None))
        self.scheduler_instrument_refresh = SchedulerVsaInstrumentsRefresh(self.implied_volatility_queue)
        self.service_implied_volatility_queue_manager = ServiceImpliedVolatilityQueueManager(self.implied_volatility_queue)
        self.service_deribit_observer_bsm_implied_volatility_manager = ServiceImpliedVolatilityObserverManager(self.implied_volatility_queue)
        
    def create_producer(self, currency: str):
        inner_loop_thread = threading.Thread(target=self.run_scheduler(currency=currency), name='vsa_producer')
        inner_loop_thread.start()
        loop_run_forever_log_exception(loop = asyncio.new_event_loop(), awaitable=self.service_implied_volatility_queue_manager.manage_implied_volatility_queue()
                                       , logger=logger, origin=f"{self.__class__.__name__} create_producer")

    def run_scheduler(self, currency: str):
        thread_2_loop = asyncio.new_event_loop()
        loop_run_forever_log_exception(loop=thread_2_loop, awaitable=self.build_vsa_tasks(currency=currency), logger=logger, origin=f"{self.__class__.__name__} Scheduler")
        
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
