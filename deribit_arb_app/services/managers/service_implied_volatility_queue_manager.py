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

    def __init__(self, 
                 implied_volatility_queue:asyncio.Queue) -> None:
        self.vsa_created                 = False
        self.implied_volatility_cache    = deque()
        self.implied_volatility_queue    = implied_volatility_queue
        self.service_vsa_object_manager  = ServiceImpliedVolatiltySurfaceAreaObjectManager()
        
        
    async def manage_implied_volatility_queue(self,
                                              plot: bool):
        """
        Asynchronously manages the implied volatility queue, creating or updating the VSA object as necessary.
        """
        
        logger.info(f"{self.__class__.__name__}: Running ")
        while True:
            try:
                # Process items in the queue if it's not empty
                if self.implied_volatility_queue.qsize() > 0:
                    model_iv_object = self.implied_volatility_queue.get_nowait()
                    
                    required_fields = ['strike', 'time_to_maturity', 'implied_volatility', 'option_type']
                    # Required fields for a valid implied volatility object
                    if not (isinstance(model_iv_object, ModelIndicatorBsmImpliedVolatility) and 
                        all(hasattr(model_iv_object, field) for field in required_fields)):
                        logger.error(f"{self.__class__.__name__}:"\
                            f"Incorrect object or missing fields received in implied_volatility_queue")
                        continue
                    
                    ## if all checks pass add to cache
                    self.implied_volatility_cache.append(model_iv_object)
                    
                    # if not vsa_created and cache is of adequete size, trigger initial creation of vsa object
                    if len(self.implied_volatility_cache) >= 50 and not self.vsa_created:
                        # Assign current cache to a local variable
                        current_cache = self.implied_volatility_cache
                        # Clear the cache
                        self.implied_volatility_cache = deque()

                        # Use the local variable for task deployment
                        task = self.service_vsa_object_manager.create_vsa_surface(plot=plot,
                                                                                  model_iv_objects=current_cache)
                        asyncio_create_task_log_exception(
                            logger=logger,
                            awaitable=task,
                            origin=f"{self.__class__.__name__} manage_iv_queue")
                        self.vsa_created = True
                    
                    # if  vsa_created and cache is of adequete size, trigger update of vsa object
                    if self.vsa_created and len(self.implied_volatility_cache) >= 10:
                        # Assign current cache to a local variable
                        current_cache = self.implied_volatility_cache
                        # Clear the cache
                        self.implied_volatility_cache = deque()

                        # Use the local variable for task deployment
                        task = self.service_vsa_object_manager.update_vsa_surface(model_iv_objects=current_cache)
                        asyncio_create_task_log_exception(
                                                          logger=logger,
                                                          awaitable=task,
                                                          origin=f"{self.__class__.__name__} manage_iv_queue")
                    
            except Exception as e:
                logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                        f"Stack trace: {traceback.format_exc()}")