import time
import asyncio
import threading

from singleton_decorator import singleton

from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility

    ####################################################################################################
    # Service Manages the implied_volatility_queue process which must be called from a seperate thread # 
    ####################################################################################################
    
@singleton
class ServiceDeribitBsmImpliedVolatilityQueueManager():
    
    def __init__(self, implied_volatility_queue:asyncio.Queue) -> None:
        self.implied_volatility_dict = {}
        self.implied_volatility_queue = implied_volatility_queue
        
    def create(self) -> asyncio.Queue[ModelIndicatorBsmImpliedVolatility]:
        inner_loop_thread = threading.Thread(target=lambda: self.manage_implied_volatility_queue())
        inner_loop_thread.start()

    def manage_implied_volatility_queue(self) -> asyncio.Queue[ModelIndicatorBsmImpliedVolatility]:
        while True:
            if self.implied_volatility_queue.qsize() > 0:
                while self.implied_volatility_queue.qsize() > 0:
                    model_iv_object = self.implied_volatility_queue.get_nowait()
                    self.implied_volatility_dict[model_iv_object.name] = model_iv_object 
                    print(self.implied_volatility_dict)
            time.sleep(0)