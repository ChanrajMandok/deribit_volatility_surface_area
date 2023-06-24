import os
import asyncio
import traceback

from typing import List, Tuple, Optional
from singleton_decorator import singleton

from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.model.model_subscribable_instrument import ModelSubscribableInstrument
from deribit_arb_app.services.deribit_api.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.services.retrievers.service_deribit_liquid_instruments_retriever import ServiceDeribitLiquidInstrumentsRetriever
    
    ##########################################################################
    # Service Handles & Manages instrument subscriptions and Unsubscriptions # 
    ##########################################################################

@singleton
class ServiceInstrumentsSubscriptionManager():
    
    def __init__(self, instruments_queue:asyncio.Queue):
        self.previous_instruments = None
        self.instruments_queue = instruments_queue
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.instruments_refresh_increment = os.environ['INSTRUMENTS_REFRESH']
        self.liquid_instruments_retriever = ServiceDeribitLiquidInstrumentsRetriever()
        
    async def manage_instrument_subscribables(self, 
                                              currency: str,
                                              kind: str,
                                              index: Optional[ModelSubscribableIndex],
                                              minimum_liquidity_threshold: int
                                              ) -> Tuple[List[ModelSubscribableIndex], List[ModelSubscribableIndex], List[ModelSubscribableIndex]]:
        if index:
            index_subscribed = False

        while True:
            instruments = await self.liquid_instruments_retriever.main(kind=kind,
                                                                    populate=False,
                                                                    currency=currency,
                                                                    minimum_liquidity_threshold=minimum_liquidity_threshold)

            instrument_names = self.__get_instrument_names(instruments=instruments)

            if index and not index_subscribed:
                instruments.insert(0, index)
                instrument_names.insert(0, index.name)
                index_subscribed = True

            if self.previous_instruments is None:
                instruments_subscribables = instruments
                instruments_unsubscribables = []
            else:
                previous_instrument_names = self.__get_instrument_names(instruments=self.previous_instruments)
                instruments_subscribables = [instrument for instrument in instruments if instrument.name not in previous_instrument_names]
                instruments_unsubscribables = [instrument for instrument in self.previous_instruments if instrument.name not in instrument_names]

            self.previous_instruments = instruments
            # print(len(instruments_subscribables), len(instruments_unsubscribables))
            await self.instruments_queue.put((instruments_subscribables, instruments_unsubscribables))
            await asyncio.sleep(360)
            
    def __get_instrument_names(self, instruments):
        return [instrument.name for instrument in instruments]

    async def a_coroutine_subscribe(self, subscribables: List[ModelSubscribableInstrument]):
        try:
            await self.deribit_subscribe.subscribe(subscribables=subscribables, snapshot=False)
        except asyncio.exceptions.TimeoutError:
            pass
        except Exception:
            traceback.print_exc()

    async def a_coroutine_unsubscribe(self, unsubscribables: List[ModelSubscribableInstrument]): 
        await self.deribit_subscribe.unsubscribe(unsubscribables=unsubscribables)