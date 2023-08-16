import asyncio
from typing import Optional

from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.model.model_subscribable_volatility_index import ModelSubscribableVolatilityIndex
from deribit_arb_app.observers.observer_store_observable_instrument_list import ObserverStoreObservableInstrumentList
from deribit_arb_app.services.retrievers.service_deribit_vsa_instruments_retriever_ws import ServiceDeribitVsaInstrumentsRetrieverWs
from deribit_arb_app.converters.convert_instruments_list_to_model_observable_instrument_list import ConvertInstrumentsListToModelObservableInstrumentList

    ###########################################################################################
    # Task run by schedular to provide instrument model subscribables to subscription Manager # 
    ###########################################################################################
    
@singleton
class TaskUpdateVsaInstrumentsStore:
    
    def __init__(self, implied_volatility_queue: asyncio.Queue) -> None:
        self.store_observable_instrument_list = Stores.store_observable_instrument_list
        self.vsa_instruments_retriever  = ServiceDeribitVsaInstrumentsRetrieverWs()
        self.observer_store_observable_instrument_list = ObserverStoreObservableInstrumentList(implied_volatility_queue)
        self.convert_instruments_list_to_model_observable_instrument_list = \
            ConvertInstrumentsListToModelObservableInstrumentList()
        
    async def update(self,
               kind: str,
               currency: str,
               minimum_liquidity_threshold: int,
               index: Optional[ModelSubscribableIndex],
               volatility_index: Optional[ModelSubscribableVolatilityIndex]):
        
        if index:
            index_subscribed = False
            
        if volatility_index:
            volatility_index_subscribed = False
        
        instruments = await self.vsa_instruments_retriever.main(kind=kind,
                                                                currency=currency,
                                                                minimum_liquidity_threshold=minimum_liquidity_threshold)
        
        subscriptions = [(index_subscribed, index), (volatility_index_subscribed, volatility_index)]
        for subs, indexes in subscriptions:
            if not subs:
                instruments.insert(0, indexes)
                subs = True
                
        moil = self.convert_instruments_list_to_model_observable_instrument_list.convert(instruments=instruments)
        
        if self.store_observable_instrument_list.__len__() == 0:
            self.observer_store_observable_instrument_list.attach_observer(moil)
                   
        self.store_observable_instrument_list.update_observable(observable_instance=moil)
        print('store_udpated')
        
        
        
        