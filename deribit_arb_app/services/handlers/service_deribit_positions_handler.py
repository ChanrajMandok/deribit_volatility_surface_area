from singleton_decorator import singleton

from deribit_arb_app.services import logger

from deribit_arb_app.converters.converter_json_to_positions import \
                                       ConverterJsonToModelPositions
from deribit_arb_app.store.store_deribit_positions import StoreDeribitPositions
from deribit_arb_app.services.handlers.service_deribit_handler_interface import ServiceDeribitHanderInterface

    ######################################
    # Service handles Deribit Positions  #
    ######################################

@singleton
class ServiceDeribitPositionsHandler(ServiceDeribitHanderInterface):
    """
    Singleton class responsible for handling the state and operations
    related to Deribit positions.
    """
        
    def __init__(self) -> None:
        self.__logger_instance = logger
        self.__store_instance = StoreDeribitPositions()
        self.__converter_instance = ConverterJsonToModelPositions
    
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