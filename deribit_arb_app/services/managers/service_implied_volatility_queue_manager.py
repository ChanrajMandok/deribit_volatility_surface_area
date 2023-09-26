import asyncio

from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import \
                                                         ModelIndicatorBsmImpliedVolatility

    #######################################################################
    # Service Manages the implied_volatility_queue from a seperate thread # 
    #######################################################################
    
@singleton
class ServiceImpliedVolatilityQueueManager():

    def __init__(self, implied_volatility_queue:asyncio.Queue) -> None:
        self.plot_created = False
        self.implied_volatility_cache = []
        self.implied_volatility_queue = implied_volatility_queue
        
    async def manage_implied_volatility_queue(self):
        while True:
            try:
                if self.implied_volatility_queue.qsize() > 0:
                    model_iv_object = self.implied_volatility_queue.get_nowait()
                    
                    required_fields = ['strike', 'time_to_maturity', 'implied_volatility', 'option_type']
                    if not (isinstance(model_iv_object, ModelIndicatorBsmImpliedVolatility) and 
                        all(hasattr(model_iv_object, field) for field in required_fields)):
                        logger.error(f"{self.__class__.__name__}: Incorrect object or missing fields received in implied_volatility_queue")
                        continue
                    
                    ## if all checks pass add to cache
                    self.implied_volatility_cache.append(model_iv_object)
                    
                    ## if plot not produced and cache is of good size, tirgger initial creation of plot
                    if len(self.implied_volatility_cache) >= 20 and not self.plot_created:
                        ## cache will be emptied and all parsed into no.arrays then ploted
                        pass
                    ## next if plot is created, the call the update function which will update plot
                    if self.plot_created == True:
                        ## cache will be emptied and all parsed into no.arrays then used to update plot
                        pass
                    
            except Exception as e:
                logger.error(f"{self.__class__.__name__}: Error in manage_implied_volatility_queue: {e}")