import asyncio

from singleton_decorator import singleton

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
        
    async def manage_implied_volatility_queue(self) -> asyncio.Queue[ModelIndicatorBsmImpliedVolatility]:
        while True:
            if self.implied_volatility_queue.qsize() > 0:
                    model_iv_object = self.implied_volatility_queue.get_nowait()
                    if not isinstance(model_iv_object, ModelIndicatorBsmImpliedVolatility):
                        continue
                    ttm = round(model_iv_object.time_to_maturity,4)
                    
                    self.implied_volatility_dict[(model_iv_object.strike, ttm)] = \
                                                                                   model_iv_object.implied_volatility
                    print(f'{model_iv_object.name} : {model_iv_object.implied_volatility}')
            else: 
                await asyncio.sleep(1)