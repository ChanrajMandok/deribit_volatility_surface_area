import os
import asyncio
import traceback

from typing import List, Tuple,Optional
from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.model.model_subscribable_instrument import ModelSubscribableInstrument
from deribit_arb_app.services.deribit_api.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.model.model_subscribable_volatility_index import ModelSubscribableVolatilityIndex
from deribit_arb_app.services.retrievers.service_deribit_vsa_instruments_retriever import ServiceDeribitVsaInstrumentsRetriever
    
    ##########################################################################
    # Service Handles & Manages instrument subscriptions and Unsubscriptions # 
    ##########################################################################

@singleton
class ServiceInstrumentsSubscriptionManager():
    
    def __init__(self, instruments_queue:asyncio.Queue):
        self.instruments_queue = instruments_queue
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.previous_instruments_store = Stores.store_instrument_list
        self.liquid_instruments_retriever = ServiceDeribitVsaInstrumentsRetriever()
        
    async def manage_instrument_subscribables(self, 
                                              kind: str,
                                              currency: str,
                                              minimum_liquidity_threshold: int,
                                              index: Optional[ModelSubscribableIndex],
                                              volatility_index: Optional[ModelSubscribableVolatilityIndex],
                                              ) ->  asyncio.Queue(Tuple[List[ModelSubscribableIndex], List[ModelSubscribableIndex]]):
        
        previous_instruments = self.previous_instruments_store.get_all()
        
        if index:
            index_subscribed = False
            
        if volatility_index:
            volatility_index_subscribed = False

        instruments = await self.liquid_instruments_retriever.main(kind=kind,
                                                                populate=False,
                                                                currency=currency,
                                                                minimum_liquidity_threshold=minimum_liquidity_threshold)

        instrument_names = self.__get_instrument_names(instruments=instruments)

        subscriptions = [(index_subscribed, index), (volatility_index_subscribed, volatility_index)]
        for subscribed, index in subscriptions:
            if not subscribed:
                instruments.insert(0, index)
                instrument_names.insert(0, index.name)
                subscribed = True

        if len(previous_instruments) == 0:
            instruments_subscribables = instruments
            instruments_unsubscribables = []
        else:
            previous_instrument_names = previous_instruments
            instruments_subscribables = [instrument for instrument in instruments if instrument.name not in previous_instrument_names]
            instruments_unsubscribables = [instrument for instrument in previous_instruments if instrument not in instrument_names]

        self.previous_instruments_store.update(instrument_names)
        print(len(instruments_subscribables), len(instruments_unsubscribables))
        await self.instruments_queue.put((instruments_subscribables, instruments_unsubscribables))
            
    def __get_instrument_names(self, instruments):
        return [instrument.name for instrument in instruments]

