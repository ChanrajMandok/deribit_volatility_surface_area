from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_get_interface import \
                                                      ServiceDeribitGetInterface
                                                      
    #####################################################################
    # Service Retrieves Deribit index price by index name via Websocket #
    #####################################################################

@singleton
class ServiceDeribitGetIndexPriceByIndexName(ServiceDeribitGetInterface):
    """
    Service class to fetch the index price by index name from Deribit.
    """
    
    def __init__(self,
                 index_currency: EnumIndexCurrency) -> None:
        self._logger_instance = logger
        self.index_currency = index_currency
        self.deribit_messaging = ServiceDeribitMessaging()
    
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def params(self):
        params = {"index_name": self.index_currency.value}
        return params
        
    @property
    def method(self):
        method = "public/get_index_price"
        return method