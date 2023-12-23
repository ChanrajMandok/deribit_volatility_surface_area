from singleton_decorator import singleton

from deribit_arb_app.services import logger

from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_get_interface import \
                                                      ServiceDeribitGetInterface

    #####################################################
    # Service Retrieves Deribit Positions via Websocket #
    #####################################################

@singleton
class ServiceDeribitPositions(ServiceDeribitGetInterface):
    """
    Service for retrieving positions from Deribit via Websocket.
    """

    def __init__(self, 
                 kind: str,
                 currency: str):
        self.kind = kind
        self.currency = currency
        self._logger_instance = logger
        self.deribit_messaging = ServiceDeribitMessaging()
        
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def params(self):
        params ={"kind": self.kind,
                 "currency": self.currency
                }
        return params
        
    @property
    def method(self):
        method = "private/get_positions"
        return method