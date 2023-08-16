import asyncio

from typing import List, Optional
from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.utils.utils_asyncio import (asyncio_create_task_log_exception)
from deribit_arb_app.services.deribit_api.service_api_deribit_utils import ServiceApiDeribitUtils
from deribit_arb_app.services.deribit_api.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.model.model_subscribable_instrument import ModelSubscribableInstrument
from deribit_arb_app.model.model_subscribable_volatility_index import ModelSubscribableVolatilityIndex
from deribit_arb_app.services.managers.service_implied_volatility_observer_manager import ServiceImpliedVolatilityObserverManager    
from deribit_arb_app.services.retrievers.service_deribit_vsa_instruments_retriever_ws import ServiceDeribitVsaInstrumentsRetrieverWs

    ##########################################################################
    # Service Handles & Manages instrument subscriptions and Unsubscriptions # 
    ##########################################################################

@singleton
class ServiceInstrumentsSubscriptionManager():
    
    def __init__(self, implied_volatility_queue: asyncio.Queue):
        self.implied_volatility_queue   = implied_volatility_queue
        self.service_api_deribit_utils  = ServiceApiDeribitUtils()
        self.service_deribit_subscribe = ServiceDeribitSubscribe()
        self.vsa_instruments_retriever  = ServiceDeribitVsaInstrumentsRetrieverWs()
        self.store_observable_instrument_list = Stores.store_observable_instrument_list
        self.service_deribit_observer_bsm_implied_volatility_manager = ServiceImpliedVolatilityObserverManager(self.implied_volatility_queue)
        
    async def manage_instrument_subscribables(self,
                                              instruments: Optional[List[ModelSubscribableInstrument]], 
                                              index: Optional[ModelSubscribableIndex],
                                              volatility_index: Optional[ModelSubscribableVolatilityIndex]):
              
        if index:
            index_subscribed = False
            
        if volatility_index:
            volatility_index_subscribed = False
        
        subscriptions = [(index_subscribed, index), (volatility_index_subscribed, volatility_index)]
        for subscribed, index in subscriptions:
            if not subscribed:
                instruments.insert(0, index)
                instrument_names.insert(0, index.name)
                subscribed = True

        previous_instruments = self.service_deribit_subscribe.get_subscriptions()
        instrument_names = self.__get_instrument_names(instruments=instruments)
        
        if len(previous_instruments) == 0:
            instruments_subscribables = instruments
            instruments_unsubscribables = []
        else:
            previous_instrument_names = previous_instruments
            instruments_subscribables = [instrument for instrument in instruments if instrument.name not in previous_instrument_names]
            instruments_unsubscribables = [instrument for instrument in previous_instruments if instrument not in instrument_names]

        # self.previous_instruments_store.update(instrument_names)
        print(len(instruments_subscribables), len(instruments_unsubscribables))
        
        try:
            if len(instruments_subscribables) > 0:
                asyncio_create_task_log_exception(awaitable=self.service_api_deribit_utils.a_coroutine_subscribe(subscribables=instruments_subscribables),
                                                                                                                logger=logger, origin="a_coroutine_subscribe")
            if len(instruments_unsubscribables) > 0:
                asyncio_create_task_log_exception(awaitable=self.service_api_deribit_utils.a_coroutine_unsubscribe(unsubscribables=instruments_unsubscribables),
                                                                                                                logger=logger, origin="a_coroutine_unsubscribe")
            if len(instruments_subscribables) > 0 or len(instruments_unsubscribables) > 0:
                asyncio_create_task_log_exception(awaitable=self.service_deribit_observer_bsm_implied_volatility_manager.manager_observers(index=index,
                                                                                                                                 volatility_index=volatility_index,
                                                                                                                                 subscribables=instruments_subscribables,
                                                                                                                                 unsubscribables=instruments_unsubscribables),
                                                                                                                                    logger=logger, origin="manager_observers")
        except Exception as e:
            print(f"Exception in run_strategy: {e}")
                 
    def __get_instrument_names(self, instruments):
        return [instrument.name for instrument in instruments]

