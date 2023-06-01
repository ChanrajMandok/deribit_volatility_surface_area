import time
import asyncio

from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility

    ###################################################################################################
    # Service Manages the implied_volatility_queue process which must be called from a seperate thread # 
    ###################################################################################################

class ServiceDeribitBsmImpliedVolatilityQueueManager():

    def manage_implied_volatility_queue(self, implied_volatility_queue: asyncio.Queue) -> asyncio.Queue[ModelIndicatorBsmImpliedVolatility]:
        while True:
            if implied_volatility_queue.qsize() > 0:
                while implied_volatility_queue.qsize() > 0:
                    model_iv_object = implied_volatility_queue.get_nowait()
                    if all(hasattr(model_iv_object, attr) for attr in ['implied_volatilty', 'strike', 'spot', 'time_to_maturity']):
                        print(model_iv_object.implied_volatilty, model_iv_object.strike, model_iv_object.spot, model_iv_object.time_to_maturity)
            time.sleep(0)