import os
import tzlocal
import asyncio

from typing import Optional
from singleton_decorator import singleton
from deribit_arb_app.schedulers import logger
from apscheduler.schedulers.background import BackgroundScheduler
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.utils.utils_asyncio import (asyncio_create_task_log_exception)
from deribit_arb_app.model.model_subscribable_volatility_index import ModelSubscribableVolatilityIndex
from deribit_arb_app.services.managers.service_instruments_subscription_manager import ServiceInstrumentsSubscriptionManager

    ######################################################################
    # Service Schedules Update of the Instrument constituents of the VSA # 
    ######################################################################

@singleton
class SchedulerVsaInstrumentsRefresh():
    
    def __init__(self, instruments_queue:asyncio.Queue) -> None:
        self.instruments_queue = instruments_queue
        self.__sched = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
        self.__refresh_increment_mins = int(os.environ['INSTRUMENTS_REFRESH_MINS'])
        self.instruments_subscription_manager = ServiceInstrumentsSubscriptionManager(self.instruments_queue)

    def scheduled_task(self, 
                    currency: str,
                    kind: str,
                    index: Optional[ModelSubscribableIndex],
                    volatility_index: Optional[ModelSubscribableVolatilityIndex],
                    minimum_liquidity_threshold: int):
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Create the task but don't run it yet
        task = self.instruments_subscription_manager.manage_instrument_subscribables(
            kind=kind,
            index=index,
            volatility_index=volatility_index,
            currency=currency,
            minimum_liquidity_threshold=minimum_liquidity_threshold
        )
        
        # Run the task until it completes
        loop.run_until_complete(task)

    def run(self, 
            currency: str,
            kind: str,
            index: Optional[ModelSubscribableIndex],
            volatility_index: Optional[ModelSubscribableVolatilityIndex],
            minimum_liquidity_threshold: int):

        logger.info(f"{__class__.__name__}: Starting scheduler...")
        self.__sched.start()
        self.__sched.add_job(self.scheduled_task, 'cron', 
                             minute=f"*/{self.__refresh_increment_mins}",
                             args=[currency, kind, index, 
                             volatility_index, minimum_liquidity_threshold])
