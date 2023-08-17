import asyncio
import threading

from typing import List, Optional
from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.model.model_subscribable_instrument import ModelSubscribableInstrument
from deribit_arb_app.model.model_observable_instrument_list import ModelObservableInstrumentList
from deribit_arb_app.services.deribit_api.service_api_deribit_utils import ServiceApiDeribitUtils
from deribit_arb_app.model.model_subscribable_volatility_index import ModelSubscribableVolatilityIndex
from deribit_arb_app.services.retrievers.service_deribit_vsa_instruments_retriever_ws import ServiceDeribitVsaInstrumentsRetrieverWs
from deribit_arb_app.utils.utils_asyncio import loop_create_task_log_exception, get_or_create_eventloop, asyncio_create_task_log_exception 

    ##########################################################################
    # Service Handles & Manages instrument subscriptions and Unsubscriptions # 
    ##########################################################################

@singleton
class ServiceInstrumentsSubscriptionManager():
    
    def __init__(self, implied_volatility_queue: asyncio.Queue, instruments_queue: asyncio.Queue):
        self.previous_instruments             = []
        self.instruments_queue                = instruments_queue
        self.implied_volatility_queue         = implied_volatility_queue
        self.service_api_deribit_utils        = ServiceApiDeribitUtils()
        self.vsa_instruments_retriever        = ServiceDeribitVsaInstrumentsRetrieverWs()
        self.store_observable_instrument_list = Stores.store_observable_instrument_list
        
    async def manage_instruments_queue(self):
        logger.info(f"{self.__class__.__name__} running ")

        while True:
            if not self.instruments_queue.empty():
                model_observable_instrument_list = await self.instruments_queue.get()

                if not isinstance(model_observable_instrument_list, ModelObservableInstrumentList):
                    raise Exception(f"{self.__class__.__name__} queue not popualted with model instances")

                task = self.manage_instrument_subscribables(
                    index=model_observable_instrument_list.index,
                    volatility_index=model_observable_instrument_list.volatility_index,
                    instruments=model_observable_instrument_list.instruments)

                asyncio_create_task_log_exception(awaitable=task, logger=logger, 
                                                  origin=f"{self.__class__.__name__} manage_instruments_queue")
            else:
                await asyncio.sleep(1)

    async def manage_instrument_subscribables(self,
                                              instruments: Optional[List[ModelSubscribableInstrument]], 
                                              index: Optional[ModelSubscribableIndex],
                                              volatility_index: Optional[ModelSubscribableVolatilityIndex]):
        try:      

            instrument_names = self.__get_instrument_names(instruments=instruments)

            subscriptions = []
            if index:
                subscriptions.append((False, index))
            if volatility_index:
                subscriptions.append((False, volatility_index))

            for subscribed, inst in subscriptions:
                if not subscribed:
                    instruments.insert(0, inst)
                    instrument_names.insert(0, inst.name)

        except Exception as e:
            raise Exception(f"{self.__class__.__name__}: {e}")
        
        try:    
            if len(self.previous_instruments) == 0:
                self.previous_instruments = instruments
                instruments_subscribables = instruments
                instruments_unsubscribables = []
            else:
                previous_instrument_names = self.previous_instruments
                instruments_subscribables = [instrument for instrument in instruments if instrument.name not in previous_instrument_names]
                instruments_unsubscribables = [instrument for instrument in self.previous_instruments if instrument not in instrument_names]
        except Exception as e:
            raise Exception(f"{self.__class__.__name__}: {e}")

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
            raise Exception(f"{self.__class__.__name__}: {e}")
                 
    def __get_instrument_names(self, instruments):
        return [instrument.name for instrument in instruments]

