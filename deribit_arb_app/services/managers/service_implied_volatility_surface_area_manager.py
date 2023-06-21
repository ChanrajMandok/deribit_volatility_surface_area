import os
import asyncio

from singleton_decorator import singleton
from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency
from deribit_arb_app.services.managers.service_implied_volatility_queue_manager import ServiceImpliedVolatilityQueueManager
from deribit_arb_app.services.managers.servicet_instruments_subscription_manager import ServiceInstrumentsSubscriptionManager
from deribit_arb_app.services.managers.service_observer_bsm_implied_volatility_manager import ServiceObserverBsmImpliedVolatilityManager

    ########################################################################################################################
    # Service runs all tasks to construct Volatility Surface area -> Instument subscriptions, Observers and Asyncio Queues #
    ########################################################################################################################

@singleton
class ServiceImpliedVolatilitySurfaceAreaManager():
    
    def __init__(self):
        self.instruments_queue = asyncio.Queue()
        self.implied_volatility_queue = asyncio.Queue()
        self.minimum_liquidity_threshold = os.environ.get('VSA_MINIMUM_LIQUIDITY_THRESHOLD', None)
        self.service_implied_volatility_queue_manager = ServiceImpliedVolatilityQueueManager(self.implied_volatility_queue)
        self.service_deribit_instruments_subscription_manager = ServiceInstrumentsSubscriptionManager(self.instruments_queue)
        self.service_deribit_observer_bsm_implied_volatility_manager = ServiceObserverBsmImpliedVolatilityManager(self.implied_volatility_queue)
        
    async def build_vsa(self, currency: str, kind: str):
        index_currency_value = getattr(EnumIndexCurrency, currency.upper()).value
        index = ModelIndex(index_name=index_currency_value)

        # This triggers the producer in the self.instruments_queue -> asyncio.Queue() object 
        asyncio.create_task(self.service_deribit_instruments_subscription_manager.manage_instrument_subscribables(kind=kind,
                                                                                                                  index=index,
                                                                                                                  currency=currency,
                                                                                                                  minimum_liquidity_threshold=self.minimum_liquidity_threshold
                                                                                                                   ))  
                
        while True:
            try:
                # This is the consumer in the self.instruments_queue -> asyncio.Queue() object
                while self.instruments_queue.qsize() > 1:
                    await self.instruments_queue.get()
                    self.instruments_queue.task_done()
                
                # This is the consumer in the self.instruments_queue -> asyncio.Queue() object
                instruments_subscribe, instruments_unsubscribe = await self.instruments_queue.get()
                if len(instruments_subscribe) > 0:
                    subscribe_task = asyncio.create_task(self.service_deribit_instruments_subscription_manager.a_coroutine_subscribe(subscribables=instruments_subscribe))
                if len(instruments_unsubscribe) > 0:
                    unsubscribe_task = asyncio.create_task(self.service_deribit_instruments_subscription_manager.a_coroutine_unsubscribe(unsubscribables=instruments_unsubscribe))
                if len(instruments_subscribe) > 0 or len(instruments_unsubscribe) > 0:
                    producer_observer_task = asyncio.create_task(self.service_deribit_observer_bsm_implied_volatility_manager.manager_observers(index=index,
                                                                                                                                               subscribables=instruments_subscribe,
                                                                                                                                               unsubscribables=instruments_unsubscribe
                                                                                                                                              ))
                threaded_consumer = self.service_implied_volatility_queue_manager.create_consumer()
            except Exception as e:
                print(f"Exception in run_strategy: {e}")
                continue
