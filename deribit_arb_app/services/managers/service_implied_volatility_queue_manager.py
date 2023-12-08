import os
import asyncio
import traceback

from collections import deque
from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.utils.utils_asyncio import asyncio_create_task_log_exception
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import \
                                                         ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.services.managers.service_implied_volatilty_surface_area_object_manager import \
                                                      ServiceImpliedVolatiltySurfaceAreaObjectManager

    #######################################################################
    # Service Manages the implied_volatility_queue from a seperate thread # 
    #######################################################################
    
@singleton
class ServiceImpliedVolatilityQueueManager():
    """
    Manages the queue of implied volatility indicators and handles the creation and updating
    of the volatility surface area (VSA) object based on these indicators.
    """

    def __init__(self, implied_volatility_queue:asyncio.Queue) -> None:
        self.vsa_created = False
        self.implied_volatility_cache = {}  
        self.implied_volatility_queue = implied_volatility_queue
        self.service_vsa_object_manager = ServiceImpliedVolatiltySurfaceAreaObjectManager()
        self.__vsa_max_num_subscriptions = int(os.environ.get('VSA_MAX_NUMBER_OF_SUBSCRIPTIONS', 25))
        self.__vsa_update_increment_max = int(self.__vsa_max_num_subscriptions / 2.25)
        
    async def manage_implied_volatility_queue(self, plot: bool):
        """
        Asynchronously manages the implied volatility queue, creating or updating the VSA object as necessary.
        """
        logger.info(f"{self.__class__.__name__}: Running ")
        while True:
            try:
                if self.implied_volatility_queue.qsize() > 0:
                    model_iv_object = await self.implied_volatility_queue.get()
                    instrument_name = model_iv_object.instrument.name 
                    
                    required_fields = ['strike', 'time_to_maturity', 'implied_volatility', 'option_type']
                    if not (isinstance(model_iv_object, ModelIndicatorBsmImpliedVolatility) and 
                        all(hasattr(model_iv_object, field) for field in required_fields)):
                        logger.error(f"{self.__class__.__name__}: Incorrect object or missing fields received")
                        continue

                    # Update cache with the latest object
                    self.implied_volatility_cache[instrument_name] = model_iv_object
                    
                    # Check if it's time to create or update the VSA
                    if (len(self.implied_volatility_cache) >= self.__vsa_update_increment_max):
                        if not self.vsa_created:
                            # Creating VSA for the first time
                            task = self.service_vsa_object_manager.create_vsa_surface(
                                        plot=plot,
                                        model_iv_objects=list(self.implied_volatility_cache.values()))
                            self.vsa_created = True
                        else:
                            # Updating existing VSA
                            task = self.service_vsa_object_manager.update_vsa_surface(
                                model_iv_objects=list(self.implied_volatility_cache.values())
                            )

                        # Handle the task asynchronously
                        asyncio_create_task_log_exception(logger=logger,
                                                          awaitable=task,
                                                          origin=f"{self.__class__.__name__} manage_iv_queue")
                        
                        # Clear the cache after task creation
                        self.implied_volatility_cache.clear()

            except Exception as e:
                logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                        f"Stack trace: {traceback.format_exc()}")