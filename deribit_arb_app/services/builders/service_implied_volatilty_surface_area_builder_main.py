import os
import time
import asyncio
import threading

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency
from deribit_arb_app.store.store_subject_indicator_bsm_implied_volatilty import StoreSubjectIndicatorBsmImpliedVolatilty
from deribit_arb_app.services.managers.service_deribit_instruments_subscription_manager import ServiceDeribitInstrumentsSubscriptionManager
from deribit_arb_app.services.managers.service_deribit_observer_bsm_implied_volatilty_manager import ServiceDeribitObserverBsmImpliedVolatilityManager
from deribit_arb_app.services.managers.service_deribit_implied_volatility_queue_manager import ServiceDeribitBsmImpliedVolatilityQueueManager

    ###########################################################################
    # Plot Subscribe, Observe and plot Asset Specific Volatility Surface Area #
    ###########################################################################

class ServiceImpliedVolatilitySurfaceAreaBuilderMain:
    
    def __init__(self):
        self.iv_queue = asyncio.Queue()
        self.instruments_queue = asyncio.Queue()
        self.minimum_liquidity_threshold = os.environ.get('VSA_MINIMUM_LIQUIDITY_THRESHOLD', None)
        self.store_subject_indicator_bsm_implied_volatilty = StoreSubjectIndicatorBsmImpliedVolatilty()
        self.service_deribit_implied_volatility_queue_manager = ServiceDeribitBsmImpliedVolatilityQueueManager()
        self.service_deribit_observer_bsm_implied_volatilty_manager = ServiceDeribitObserverBsmImpliedVolatilityManager(iv_queue=self.iv_queue)
        self.service_deribit_instruments_subscription_manager = ServiceDeribitInstrumentsSubscriptionManager(instruments_queue=self.instruments_queue)

    async def run_strategy(self, currency: str, kind: str):
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
                    producer_observer_task = asyncio.create_task(self.service_deribit_observer_bsm_implied_volatilty_manager.manager_observers(index=index,
                                                                                                                                               subscribables=instruments_subscribe,
                                                                                                                                               unsubscribables=instruments_unsubscribe
                                                                                                                                              ))
                # This creates a subprocess which allows the iv_queue to be processed and returned 
                inner_loop_thread = threading.Thread(target=lambda: self.service_deribit_implied_volatility_queue_manager.manage_iv_queue(self.iv_queue))
                inner_loop_thread.start()

            except Exception as e:
                print(f"Exception in run_strategy: {e}")
                continue
