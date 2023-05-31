import os
import asyncio

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency
from deribit_arb_app.store.store_subject_indicator_bsm_implied_volatilty import StoreSubjectIndicatorBsmImpliedVolatilty
from deribit_arb_app.services.managers.service_deribit_instruments_subscription_manager import ServiceDeribitInstrumentsSubscriptionManager
from deribit_arb_app.services.managers.service_deribit_observer_bsm_implied_volatilty_manager import ServiceDeribitObserverBsmImpliedVolatilityManager

    ###########################################################################
    # Plot Subscribe, Observe and plot Asset Specific Volatility Surface Area #
    ###########################################################################

class ServiceImpliedVolatilitySurfaceAreaBuilderMain:
    
    def __init__(self):
        self.queue = asyncio.Queue()
        self.update_queue = asyncio.Queue()
        self.store_subject_indicator_bsm_implied_volatilty = StoreSubjectIndicatorBsmImpliedVolatilty()
        self.minimum_liquidity_threshold = os.environ.get('VSA_MINIMUM_LIQUIDITY_THRESHOLD', None)
        self.service_deribit_observer_bsm_implied_volatilty_manager = ServiceDeribitObserverBsmImpliedVolatilityManager()
        self.service_deribit_instruments_subscription_manager = ServiceDeribitInstrumentsSubscriptionManager(queue=self.queue)
       
    async def consume_subjects_view(self):
        async for subject_view in self.store_subject_indicator_bsm_implied_volatilty.stream_subjects_view():
            print(list(subject_view))


    async def run_strategy(self, currency: str, kind: str):
        index_currency_value = getattr(EnumIndexCurrency, currency.upper()).value
        index = ModelIndex(index_name=index_currency_value)
        
        asyncio.create_task(self.service_deribit_instruments_subscription_manager.manage_instrument_subscribables(kind=kind,
                                                                                                                  index=index,
                                                                                                                  currency=currency,
                                                                                                                  minimum_liquidity_threshold=self.minimum_liquidity_threshold
                                                                                                                   ))  
                
        while True:
            try:
                while self.queue.qsize() > 1:
                    await self.queue.get()
                    self.queue.task_done()
                
                instruments_subscribe, instruments_unsubscribe = await self.queue.get()
                if len(instruments_subscribe) > 0:
                    subscribe_task = asyncio.create_task(self.service_deribit_instruments_subscription_manager.a_coroutine_subscribe(subscribables=instruments_subscribe))
                if len(instruments_unsubscribe) > 0:
                    unsubscribe_task = asyncio.create_task(self.service_deribit_instruments_subscription_manager.a_coroutine_unsubscribe(unsubscribables=instruments_unsubscribe))
                if len(instruments_subscribe) > 0 or len(instruments_unsubscribe) > 0:
                    observer_task = asyncio.create_task(self.service_deribit_observer_bsm_implied_volatilty_manager.manager_observers(index=index,
                                                                                                                                      subscribables=instruments_subscribe,
                                                                                                                                      unsubscribables=instruments_unsubscribe
                                                                                                                                      ))
                p = asyncio.create_task(self.consume_subjects_view())
            except Exception as e:
                print(f"Exception in run_strategy: {e}")
                break