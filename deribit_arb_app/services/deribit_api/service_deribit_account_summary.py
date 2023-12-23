import json

from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_get_interface import \
                                                      ServiceDeribitGetInterface

    ###########################################################
    # Service retrieves Deribit Account Summary via Websocket #
    ###########################################################

@singleton
class ServiceDeribitAccountSummary(ServiceDeribitGetInterface):
    """
    Service class to get the account summary from Deribit.
    """ 
    def __init__(self, 
                 currency: str):
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
                 "extended": True
                }
        return params

    @property
    def method(self):
        method = "private/get_account_summary"
        return method