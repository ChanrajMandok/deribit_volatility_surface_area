import os
import tzlocal
import asyncio

from typing import Optional
from singleton_decorator import singleton

from deribit_arb_app.schedulers import logger
from deribit_arb_app.utils.utils_asyncio import \
            loop_run_until_complete_log_exception
from deribit_arb_app.model.model_subscribable_volatility_index import \
                                       ModelSubscribableVolatilityIndex
from deribit_arb_app.utils.utils_asyncio import asyncio_create_task_log_exception
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.services.managers.service_instruments_subscription_manager import \
                                                   ServiceInstrumentsSubscriptionManager
from deribit_arb_app.services.retrievers.service_deribit_vsa_instruments_retriever_ws import \
                                                       ServiceDeribitVsaInstrumentsRetrieverWs
from deribit_arb_app.converters.convert_instruments_list_to_model_observable_instrument_list import \
                                                ConvertInstrumentsListToModelObservableInstrumentList

    ######################################################################
    # Service Schedules Update of the Instrument constituents of the VSA # 
    ######################################################################

@singleton
class SchedulerVsaInstrumentsRefresh():
    
    def __init__(self, implied_volatility_queue: asyncio.Queue, instruments_queue: asyncio.Queue):
        self.instruments_queue            = instruments_queue
        self.implied_volatility_queue     = implied_volatility_queue
        self.vsa_instruments_retriever    = ServiceDeribitVsaInstrumentsRetrieverWs()
        self.__refresh_increment_mins     = int(os.environ['INSTRUMENTS_REFRESH_MINS'])
        self.convert_inst_list            = ConvertInstrumentsListToModelObservableInstrumentList()
        self.instruments_subs_manager     = ServiceInstrumentsSubscriptionManager(instruments_queue=instruments_queue,
                                                                    implied_volatility_queue= implied_volatility_queue)

    async def retrieve_and_update(self, 
                                  kind: str,
                                  currency: str,
                                  minimum_liquidity_threshold: int,
                                  index: Optional[ModelSubscribableIndex],
                                  volatility_index: Optional[ModelSubscribableVolatilityIndex]):
        while True:
            try:
                logger.info("retrieve_and_update started.")
                
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

                moil = self.convert_inst_list.convert(instruments=instruments)
                
                self.instruments_queue.put_nowait(moil)
                logger.info("retrieve_and_update completed successfully.")
                await asyncio.sleep(self.__refresh_increment_mins*60)
                
            except Exception as e:
                logger.error(f"Error in retrieve_and_update: {e}")
                await asyncio.sleep(self.__refresh_increment_mins*60)
                
    def run(self, 
            kind: str,
            currency: str,
            minimum_liquidity_threshold: int,
            index: Optional[ModelSubscribableIndex],
            volatility_index: Optional[ModelSubscribableVolatilityIndex]):

        logger.info(f"{__class__.__name__}: Starting scheduler...")
        
        asyncio.create_task(self.retrieve_and_update(kind=kind,
                                                     currency=currency,
                                                     minimum_liquidity_threshold= minimum_liquidity_threshold,
                                                     index=index,
                                                     volatility_index=volatility_index))
