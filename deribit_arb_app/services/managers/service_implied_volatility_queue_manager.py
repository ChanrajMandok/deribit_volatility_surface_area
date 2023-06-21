import time
import asyncio
import threading

from singleton_decorator import singleton

from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import ModelIndicatorBsmImpliedVolatility

    ####################################################################################################
    # Service Manages the implied_volatility_queue process which must be called from a seperate thread # 
    ####################################################################################################
    
@singleton
class ServiceImpliedVolatilityQueueManager():

    def __init__(self, implied_volatility_queue:asyncio.Queue) -> None:
        self.implied_volatility_dict = {}
        self.implied_volatility_queue = implied_volatility_queue
        
    def create_consumer(self) -> asyncio.Queue[ModelIndicatorBsmImpliedVolatility]:
        inner_loop_thread = threading.Thread(target=lambda: self.manage_implied_volatility_queue())
        inner_loop_thread.start()
        
    def manage_implied_volatility_queue(self) -> asyncio.Queue[ModelIndicatorBsmImpliedVolatility]:
        while True:
            if self.implied_volatility_queue.qsize() > 0:
                while not self.implied_volatility_queue.empty():
                    model_iv_object = self.implied_volatility_queue.get_nowait()
                    if not isinstance(model_iv_object, ModelIndicatorBsmImpliedVolatility):
                        continue
                    self.implied_volatility_dict[(model_iv_object.strike, model_iv_object.time_to_maturity)] = model_iv_object.implied_volatility
                    print(self.implied_volatility_dict)
            time.sleep(0)