import os
import asyncio
import threading

from singleton_decorator import singleton
from deribit_arb_app.services import logger
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.utils.utils_asyncio import (asyncio_create_task_log_exception)
from deribit_arb_app.enums.enum_volatility_index_currency import EnumVolatilityIndexCurrency
from deribit_arb_app.model.model_subscribable_volatility_index import ModelSubscribableVolatilityIndex
from deribit_arb_app.services.managers.service_implied_volatility_queue_manager import ServiceImpliedVolatilityQueueManager
from deribit_arb_app.services.managers.servicet_instruments_subscription_manager import ServiceInstrumentsSubscriptionManager
from deribit_arb_app.services.managers.service_implied_volatility_observer_manager import ServiceImpliedVolatilityObserverManager

    ########################################################################################################################
    # Service runs all tasks to construct Volatility Surface area -> Instument subscriptions, Observers and Asyncio Queues #
    ########################################################################################################################

@singleton
class ServiceImpliedVolatilitySurfaceAreaTaskManager():

    def __init__(self):
        self.instruments_queue = asyncio.Queue()
        self.implied_volatility_queue = asyncio.Queue()
        self.minimum_liquidity_threshold = os.environ.get('VSA_MINIMUM_LIQUIDITY_THRESHOLD', None)
        self.service_implied_volatility_queue_manager = ServiceImpliedVolatilityQueueManager(self.implied_volatility_queue)
        self.service_deribit_instruments_subscription_manager = ServiceInstrumentsSubscriptionManager(self.instruments_queue)
        self.service_deribit_observer_bsm_implied_volatility_manager = ServiceImpliedVolatilityObserverManager(self.implied_volatility_queue)
        
    def create_producer(self):
        inner_loop_thread = threading.Thread(target=lambda: asyncio.run(self.build_vsa_tasks(currency="BTC")))
        inner_loop_thread.start()
        self.service_implied_volatility_queue_manager.manage_implied_volatility_queue()
        
    async def build_vsa_tasks(self, currency: str, kind="option"):
        # function construct all task to then stream VSA via asyncio Queue to be captured by the service_implied_volatility_queue_manager
        index_currency_value = getattr(EnumIndexCurrency, currency.upper()).value
        volatility_index_currency_value = getattr(EnumVolatilityIndexCurrency, currency.upper()).value
        index = ModelSubscribableIndex(name=index_currency_value)
        volatility_index = ModelSubscribableVolatilityIndex(name=volatility_index_currency_value)

        asyncio_create_task_log_exception(self.service_deribit_instruments_subscription_manager.manage_instrument_subscribables(kind=kind,
                                                                                                                                  index=index,
                                                                                                                                  volatility_index = volatility_index,
                                                                                                                                  currency=currency,
                                                                                                                                  minimum_liquidity_threshold=self.minimum_liquidity_threshold
                                                                                                                                  ), logger, "manage_instrument_subscribables")
        while True:
            try:
                while self.instruments_queue.qsize() > 1:
                    await self.instruments_queue.get()
                    self.instruments_queue.task_done()

                instruments_subscribe, instruments_unsubscribe = await self.instruments_queue.get()
                if len(instruments_subscribe) > 0:
                    asyncio_create_task_log_exception(self.service_deribit_instruments_subscription_manager.a_coroutine_subscribe(subscribables=instruments_subscribe), logger, "a_coroutine_subscribe")
                if len(instruments_unsubscribe) > 0:
                    asyncio_create_task_log_exception(self.service_deribit_instruments_subscription_manager.a_coroutine_unsubscribe(unsubscribables=instruments_unsubscribe), logger, "a_coroutine_unsubscribe")
                if len(instruments_subscribe) > 0 or len(instruments_unsubscribe) > 0:
                    asyncio_create_task_log_exception(self.service_deribit_observer_bsm_implied_volatility_manager.manager_observers(index=index,
                                                                                                                                               volatility_index=volatility_index,
                                                                                                                                               subscribables=instruments_subscribe,
                                                                                                                                               unsubscribables=instruments_unsubscribe), logger, "manager_observers")

            except Exception as e:
                print(f"Exception in run_strategy: {e}")
                continue