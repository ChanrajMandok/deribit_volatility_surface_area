from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_get_interface import \
                                                      ServiceDeribitGetInterface

                                                      
    #######################################################
    # Service retrieves Deribit instruments via Websocket #
    #######################################################

@singleton
class ServiceDeribitInstruments(ServiceDeribitGetInterface):
    """
    Service class to fetch instruments for a specified currency and kind from Deribit.

    This class communicates with the Deribit API to retrieve a list of
    instruments, based on the specified currency and kind (e.g., 'option', 'future').
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
        params ={"currency": self.currency,
                 "kind": self.kind,
                 "expired": False
                }
        return params

    @property
    def method(self):
        method = "public/get_instruments"
        return method