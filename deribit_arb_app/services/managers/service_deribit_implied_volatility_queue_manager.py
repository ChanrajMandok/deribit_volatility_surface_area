import time
import asyncio

from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility

    ###################################################################################
    # Service Manages the iv_queue process which must be called via a seperate thread # 
    ###################################################################################

class ServiceDeribitBsmImpliedVolatilityQueueManager():

    def manage_iv_queue(self, iv_queue: asyncio.Queue) -> asyncio.Queue[ModelIndicatorBsmImpliedVolatility]:
        while True:
            if iv_queue.qsize() > 0:
                while iv_queue.qsize() > 0:
                    model_iv_object = iv_queue.get_nowait()
                    if all(hasattr(model_iv_object, attr) for attr in ['implied_volatilty', 'strike', 'spot', 'time_to_maturity']):
                        return (model_iv_object.implied_volatilty, model_iv_object.strike, model_iv_object.spot, model_iv_object.time_to_maturity)

            time.sleep(0.01)