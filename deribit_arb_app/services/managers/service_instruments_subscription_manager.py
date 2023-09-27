import os
import asyncio

from typing import Optional
from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.model.model_subscribable_volatility_index import \
                                       ModelSubscribableVolatilityIndex
from deribit_arb_app.utils.utils_asyncio import get_or_create_eventloop
from deribit_arb_app.services.deribit_api.service_api_deribit_utils import \
                                                      ServiceApiDeribitUtils
from deribit_arb_app.utils.utils_asyncio import loop_create_task_log_exception
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.utils.utils_asyncio import asyncio_create_task_log_exception
from deribit_arb_app.services.managers.service_implied_volatility_observer_manager import \
                                                    ServiceImpliedVolatilityObserverManager
from deribit_arb_app.services.retrievers.service_deribit_vsa_instruments_retriever_ws import \
                                                       ServiceDeribitVsaInstrumentsRetrieverWs

    ##########################################################################
    # Service Handles & Manages instrument subscriptions and Unsubscriptions # 
    ##########################################################################

@singleton
class ServiceInstrumentsSubscriptionManager():
    
    def __init__(self, implied_volatility_queue: asyncio.Queue):
        self.previous_instruments             = []
        self.implied_volatility_queue         = implied_volatility_queue
        self.service_api_deribit_utils        = ServiceApiDeribitUtils()
        self.store_observable_instrument_list = Stores.store_observable_instrument_list
        self.vsa_instruments_retriever        = ServiceDeribitVsaInstrumentsRetrieverWs()
        self.__refresh_increment_mins         = int(os.environ.get('INSTRUMENTS_REFRESH_SECONDS', 3600))
        self.service_bsm_observer_manager     = ServiceImpliedVolatilityObserverManager(self.implied_volatility_queue)
        
    async def manage_instruments(self, 
                                  kind: str,
                                  currency: str,
                                  minimum_liquidity_threshold: int,
                                  index: Optional[ModelSubscribableIndex],
                                  volatility_index: Optional[ModelSubscribableVolatilityIndex]):
        
            logger.info(f"{self.__class__.__name__} Running ")

            while True:
                try:
                    
                    if index:
                        index_subscribed = False

                    if volatility_index:
                        volatility_index_subscribed = False

                    instruments = \
                        await self.vsa_instruments_retriever.main(kind=kind,
                                                                  currency=currency,
                                                                  minimum_liquidity_threshold=minimum_liquidity_threshold)

                    subscriptions = [(index_subscribed, index), (volatility_index_subscribed, volatility_index)]
                    for subs, indexes in subscriptions:
                        if not subs:
                            instruments.insert(0, indexes)
                            subs = True

                    task = self.manage_instrument_subscribables(index=index,
                                                                instruments=instruments,
                                                                volatility_index=volatility_index)

                    asyncio_create_task_log_exception(logger=logger,
                                                      awaitable=task,  
                                                      origin=f"{self.__class__.__name__} manage_instruments")

                    await asyncio.sleep(self.__refresh_increment_mins)
                except Exception as e:
                    logger.error(f"{self.__class__.__name__}: manage subscriptables error")
                    await asyncio.sleep(self.__refresh_increment_mins)
                    
    async def manage_instrument_subscribables(self,
                                              instruments: Optional[list[ModelSubscribableInstrument]], 
                                              index: Optional[ModelSubscribableIndex],
                                              volatility_index: Optional[ModelSubscribableVolatilityIndex]):
        try:      

            instrument_names = self.__get_instrument_names(instruments=instruments)

        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")
        
        try:    
            if len(self.previous_instruments) == 0:
                self.previous_instruments = instruments
                instruments_subscribables = instruments
                instruments_unsubscribables = []
            else:
                previous_instrument_names = self.__get_instrument_names(instruments=self.previous_instruments)
                instruments_subscribables = \
                    [instrument for instrument in instruments if instrument.name not in previous_instrument_names]
                instruments_unsubscribables = \
                    [instrument for instrument in self.previous_instruments if instrument.name not in instrument_names]
        
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")
        
        try:
            if len(instruments_subscribables) > 0:
                asyncio_create_task_log_exception(\
                    awaitable=self.service_api_deribit_utils.a_coroutine_subscribe(subscribables=instruments_subscribables),
                                                                               logger=logger, origin="a_coroutine_subscribe")
                # logger.info(f"{len(instruments_subscribables)} instruments task subscribed ") 
            if len(instruments_unsubscribables) > 0:
                asyncio_create_task_log_exception(\
                    awaitable=self.service_api_deribit_utils.a_coroutine_unsubscribe(unsubscribables=instruments_unsubscribables),
                                                                                    logger=logger, origin="a_coroutine_unsubscribe")
                # logger.info(f"{len(instruments_unsubscribables)} instruments unsubscribed ")
            if len(instruments_subscribables) > 0 or len(instruments_unsubscribables) > 0:
                asyncio_create_task_log_exception(\
                    awaitable=self.service_bsm_observer_manager.manager_observers(index=index,
                                                                                    volatility_index=volatility_index,
                                                                                    subscribables=instruments_subscribables,
                                                                                    unsubscribables=instruments_unsubscribables),
                                                                                    logger=logger, origin="manager_observers")
        except Exception as e:
                logger.error(f"{self.__class__.__name__}: {e}")
                 
    def __get_instrument_names(self, instruments):
        return [instrument.name for instrument in instruments]