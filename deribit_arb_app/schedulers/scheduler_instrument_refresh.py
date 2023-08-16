import os
import tzlocal
import asyncio

from typing import Optional
from singleton_decorator import singleton
from deribit_arb_app.schedulers import logger
from apscheduler.schedulers.background import BackgroundScheduler
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.utils.utils_asyncio import (loop_run_until_complete_log_exception, get_or_create_eventloop)
from deribit_arb_app.model.model_subscribable_volatility_index import ModelSubscribableVolatilityIndex
from deribit_arb_app.tasks.task_update_vsa_instruments_store import TaskUpdateVsaInstrumentsStore

    ######################################################################
    # Service Schedules Update of the Instrument constituents of the VSA # 
    ######################################################################

@singleton
class SchedulerVsaInstrumentsRefresh():
    
    def __init__(self, implied_volatility_queue: asyncio.Queue) -> None:
        self.implied_volatility_queue = implied_volatility_queue
        self.__sched = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
        self.__refresh_increment_mins = int(os.environ['INSTRUMENTS_REFRESH_MINS'])
        self.__task_vsa_instruments_updater = TaskUpdateVsaInstrumentsStore(implied_volatility_queue)
        
    def scheduled_task(self, 
                    currency: str,
                    kind: str,
                    index: Optional[ModelSubscribableIndex],
                    volatility_index: Optional[ModelSubscribableVolatilityIndex],
                    minimum_liquidity_threshold: int):
        
        loop = get_or_create_eventloop()
        
        # Create the task but don't run it yet
        task = self.__task_vsa_instruments_updater.update(
                    kind=kind,
                    currency=currency,
                    minimum_liquidity_threshold=minimum_liquidity_threshold,
                    volatility_index=volatility_index,
                    index=index)
        
        # Run the task until it completes
        loop_run_until_complete_log_exception(awaitable=task, loop=loop, origin=f"{self.__class__.__name__}", logger=logger)

    def run(self, 
            currency: str,
            kind: str,
            index: Optional[ModelSubscribableIndex],
            volatility_index: Optional[ModelSubscribableVolatilityIndex],
            minimum_liquidity_threshold: int):

        logger.info(f"{__class__.__name__}: Starting scheduler...")
        self.__sched.start()
        self.__sched.add_job(self.scheduled_task, 'interval', 
                             minutes=self.__refresh_increment_mins,
                             args=[currency, kind, index, 
                             volatility_index, minimum_liquidity_threshold])
