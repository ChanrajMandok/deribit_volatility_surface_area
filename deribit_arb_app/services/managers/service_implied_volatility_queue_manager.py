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
        self.implied_volatility_dict = {}
        self.implied_volatility_queue = implied_volatility_queue
        
    async def manage_implied_volatility_queue(self):
        while True:
            try:
                if self.implied_volatility_queue.qsize() > 0:
                    
                    data = self.implied_volatility_queue.get_nowait()
                    timestamp = data["timestamp"]
                    model_iv_object = data["value"]
                    
                    if not isinstance(model_iv_object, ModelIndicatorBsmImpliedVolatility):
                        continue
                    
                    self.implied_volatility_dict[model_iv_object.strike] = {"value": model_iv_object.implied_volatility, "timestamp": timestamp}
                    
                    logger.info(f'{model_iv_object.name} : {model_iv_object.implied_volatility}')
                    
            except Exception as e:
                logger.error(f"Error in manage_implied_volatility_queue: {e}")