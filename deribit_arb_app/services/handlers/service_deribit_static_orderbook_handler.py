import json

from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.store.stores import Stores
from deribit_arb_app.services.handlers.service_deribit_handler_interface import \
                                                    ServiceDeribitHanderInterface
from deribit_arb_app.converters.converter_json_to_model_observable_order_book import \
                                               ConverterJsonToModelObservableOrderBook
                                               
    ####################################################################
    # Service handles Deribit orderbook instances retrived via aiohttp #
    ####################################################################

@singleton
class ServiceDeribitStaticOrderbookHandler(ServiceDeribitHanderInterface):
    """
    Singleton class to manage and handle the static order book operations 
    related to Deribit.
    """

    def __init__(self) -> None:
        self.__logger_instance = logger
        self.__store_instance = Stores.store_observable_orderbooks
        self.__converter_instance = ConverterJsonToModelObservableOrderBook
        
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self.__logger_instance
    
    @property
    def converter_instance(self):
        return self.__converter_instance
    
    @property
    def store_instance(self):
        return self.__store_instance