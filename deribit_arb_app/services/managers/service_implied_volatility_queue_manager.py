import time
import asyncio
import threading

from singleton_decorator import singleton
from deribit_arb_app.services.plot.service_plot_volatilty_surface_area import ServicePlotVolatilitySurfaceArea

    ####################################################################################################
    # Service Manages the implied_volatility_queue process which must be called from a seperate thread # 
    ####################################################################################################
    
class ServiceBsmImpliedVolatilityQueueManager:
    
    def __init__(self, implied_volatility_queue: asyncio.Queue):
        self.implied_volatility_dict = {}
        self.implied_volatility_queue = implied_volatility_queue
        self.service_plot_volatility_surface_area = ServicePlotVolatilitySurfaceArea()

    def create_consumer(self):
        loop = asyncio.new_event_loop()
        inner_loop_thread = threading.Thread(target=self.consume_implied_volatility_queue, args=(loop,))
        inner_loop_thread.daemon = True
        return inner_loop_thread

    def consume_implied_volatility_queue(self, event_loop):
        asyncio.set_event_loop(event_loop)
        event_loop.run_forever()

    def start_consumer(self):
        inner_loop_thread = self.create_consumer()
        inner_loop_thread.start()
        asyncio.run_coroutine_threadsafe(self.consume_implied_volatility_queue_async(), inner_loop_thread.loop())

    async def consume_implied_volatility_queue_async(self):
        while True:
            if self.implied_volatility_queue.qsize() > 0:
                while self.implied_volatility_queue.qsize() > 0:
                    model_iv_object = self.implied_volatility_queue.get_nowait()
                    model_iv_object_implied_vol = model_iv_object.implied_volatility
                    if model_iv_object.name not in self.implied_volatility_dict or \
                            self.implied_volatility_dict[model_iv_object.name].implied_volatility != model_iv_object_implied_vol:
                        self.implied_volatility_dict[model_iv_object.name] = model_iv_object
                        print(f'{model_iv_object.name}{model_iv_object.implied_volatility}')
                        
            await asyncio.sleep(10)  # Wait for 10 seconds
            await self.service_plot_volatility_surface_area.plot(poo=self.implied_volatility_dict.values())
