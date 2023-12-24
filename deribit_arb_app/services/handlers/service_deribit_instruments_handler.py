from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.store.stores import Stores
from deribit_arb_app.converters.converter_json_to_instruments import \
                                            ConverterJsonToInstruments
from deribit_arb_app.services.handlers.service_deribit_handler_interface import \
                                                    ServiceDeribitHanderInterface
                                            
    #######################################
    # Service handles Deribit instruments #
    #######################################

@singleton
class ServiceDeribitInstrumentsHandler(ServiceDeribitHanderInterface):
    """
    Singleton class to manage and handle Deribit instruments.
    """

    def __init__(self) -> None:
        self.__logger_instance = logger
        self.__converter_instance = ConverterJsonToInstruments
        self.__store_instance = Stores.store_subscribable_instruments
        
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