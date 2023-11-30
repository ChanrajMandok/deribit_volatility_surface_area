import os
import asyncio
import traceback
import threading

from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.enums.enum_volatility_index_currency import \
                                       EnumVolatilityIndexCurrency
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency
from deribit_arb_app.utils.utils_asyncio import get_or_create_eventloop
from deribit_arb_app.model.model_subscribable_volatility_index import \
                                       ModelSubscribableVolatilityIndex
from deribit_arb_app.utils.utils_asyncio import loop_run_forever_log_exception
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.utils.utils_asyncio import asyncio_create_task_log_exception
from deribit_arb_app.services.managers.service_implied_volatility_queue_manager import \
                                                    ServiceImpliedVolatilityQueueManager
from deribit_arb_app.services.managers.service_instruments_subscription_manager import \
                                                   ServiceInstrumentsSubscriptionManager

    ########################################################################################################################
    # Service runs all tasks to construct Volatility Surface area -> Instument subscriptions, Observers and Asyncio Queues #
    ########################################################################################################################

@singleton
class ServiceImpliedVolatilitySurfaceAreaTaskManager():
    """
    Manages tasks related to the implied volatility surface area, including producing and consuming
    implied volatility data, and managing subscriptions to market instruments.
    """

    def __init__(self):
        self.implied_volatility_queue = asyncio.Queue()
        self.service_iv_queue_manager = ServiceImpliedVolatilityQueueManager(self.implied_volatility_queue)
        self.service_instruments_subscription_manager = ServiceInstrumentsSubscriptionManager(self.implied_volatility_queue)


    def create_producer(self, 
                        currency: str,
                        plot:bool= False):
        """
        Creates a producer for generating tasks related to the specified currency.
        """
        logger.info(f"{self.__class__.__name__}: Running ")
        # Create a separate thread for running the instruments manager
        inner_loop_thread = threading.Thread(name='vsa_producer',
                                             target=lambda: self.run_instruments_manager(currency=currency))
        inner_loop_thread.start()
        # Run the consumer task in the main thread
        self.run_consumer(plot=plot)


    def run_instruments_manager(self,
                                currency: str):
        """
        Runs the instruments manager for a specific currency.
        """
        try:
            # Obtain or create an event loop for this thread
            thread_2_loop = get_or_create_eventloop()
            # Run the event loop forever, managing the building of VSA tasks
            loop_run_forever_log_exception(loop=thread_2_loop,
                                           awaitable=self.build_vsa_tasks(currency=currency),
                                           logger=logger, origin=f"{self.__class__.__name__} Scheduler")
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                      f"Stack trace: {traceback.format_exc()}")


    def run_consumer(self, 
                     plot:bool):
        """
        Runs the consumer task, processing implied volatility data.
        """
        if threading.current_thread() != threading.main_thread():
            raise Exception(f"{self.__class__.__name__} consumer not on main thread")
        
        # Obtain or create an event loop for the main thread
        thread_main_loop = get_or_create_eventloop()
        # Run the event loop forever, managing the consumption of implied volatility data
        loop_run_forever_log_exception(loop=thread_main_loop,
                                       awaitable=self.consumer_task(plot=plot),
                                       logger=logger, origin=f"{self.__class__.__name__} consumer")
        
        
    def get_index_and_volatility_index(self,
                                       currency: str) -> tuple[ModelSubscribableIndex, ModelSubscribableVolatilityIndex]:
        """
        Retrieves the index and volatility index based on the given currency.
        """
        # Get the index and volatility index values based on the currency
        index_currency_value = getattr(EnumIndexCurrency, currency.upper()).value
        volatility_index_currency_value = getattr(EnumVolatilityIndexCurrency,
                                                  currency.upper()).value
        
        # Create index and volatility index objects
        index = ModelSubscribableIndex(name=index_currency_value)
        volatility_index = ModelSubscribableVolatilityIndex(name=volatility_index_currency_value)
        return index, volatility_index
        
        
    async def build_vsa_tasks(self, 
                              currency: str,
                              kind="option"):
        
        """
        Asynchronously builds tasks for creating or updating the Volatility Surface Area (VSA) for a given currency.
        """
    
        index, volatility_index = self.get_index_and_volatility_index(currency=currency)
        await self.service_instruments_subscription_manager.manage_instruments(kind=kind,
                                                                               index=index,
                                                                               currency=currency,
                                                                               volatility_index = volatility_index,
                                                                               )


    async def consumer_task(self,
                            plot: bool):
        """
        Asynchronous task that consumes implied volatility data and updates the VSA.
        """
        # Manage the implied volatility queue
        iv_awaitable = self.service_iv_queue_manager.manage_implied_volatility_queue(plot=plot)
        asyncio_create_task_log_exception(awaitable=iv_awaitable,
                                          logger=logger, origin=f"{self.__class__.__name__} consume_iv_queue")