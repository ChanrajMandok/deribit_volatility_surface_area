import os
import tzlocal
import asyncio

from typing import Optional
from singleton_decorator import singleton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from deribit_arb_app.schedulers import logger
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.model.model_subscribable_volatility_index import ModelSubscribableVolatilityIndex
from deribit_arb_app.utils.utils_asyncio import (loop_run_until_complete_log_exception, get_or_create_eventloop)
from deribit_arb_app.services.retrievers.service_deribit_vsa_instruments_retriever_ws import ServiceDeribitVsaInstrumentsRetrieverWs
from deribit_arb_app.converters.convert_instruments_list_to_model_observable_instrument_list import ConvertInstrumentsListToModelObservableInstrumentList

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
        self.scheduler                    = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
        self.convert_inst_list            = ConvertInstrumentsListToModelObservableInstrumentList()
                            
    async def retrieve_and_update(self, 
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

        moil = self.convert_inst_list.convert(instruments=instruments)
        
        self.instruments_queue.put_nowait(moil)

    def run(self, 
            currency: str,
            kind: str,
            index: Optional[ModelSubscribableIndex],
            volatility_index: Optional[ModelSubscribableVolatilityIndex],
            minimum_liquidity_threshold: int):

        logger.info(f"{__class__.__name__}: Starting scheduler...")

        # Schedule the task using AsyncIOScheduler
        self.scheduler.add_job(self.retrieve_and_update, 'interval', 
                               minutes=self.__refresh_increment_mins,
                               args=[kind, currency, minimum_liquidity_threshold, index, volatility_index])
        
        # Start the scheduler
        self.scheduler.start()