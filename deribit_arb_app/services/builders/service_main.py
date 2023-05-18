import asyncio

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.services.managers.service_deribit_observer_manager import ServiceDeribitObserversManager
from deribit_arb_app.services.managers.service_deribit_instruments_subscription_manager import ServiceDeribitInstrumentsSubscriptionManager

    ###########################################################################
    # Plot Subscribe, Observe and plot Asset Specific Volatility Surface Area #
    ###########################################################################

class ServiceMain():
    def __init__(self):
        self.queue = asyncio.Queue()
        self.index = ModelIndex(index_name="btc_usd")
        self.service_deribit_observer_manager = ServiceDeribitObserversManager()
        self.service_deribit_instruments_subscription_manager = ServiceDeribitInstrumentsSubscriptionManager()
        
    async def main(self, currency: str, kind: str):
        asyncio.create_task(self.service_deribit_instruments_subscription_manager.manage_instrument_subscribables(currency, kind))  
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
                    observer_task = asyncio.create_task(self.service_deribit_observer_manager.manager_observers(subscribables=instruments_subscribe, unsubscribables=instruments_unsubscribe))    
            except Exception as e:
                print("An error occurred: %s", e, exc_info=True)