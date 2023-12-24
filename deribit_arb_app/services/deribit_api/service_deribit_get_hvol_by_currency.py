from datetime import datetime, timedelta
from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_get_interface import \
                                                      ServiceDeribitGetInterface
                                                      
    ##############################################################
    # Service Retrieves Deribit hvol by index name via Websocket #
    ##############################################################

@singleton
class ServiceDeribitGetHvolByCurrency(ServiceDeribitGetInterface):
    """
    Service class to fetch the index price by index name from Deribit.
    """
    def __init__(self,
                 currency: str) -> None:
        self._logger_instance = logger
        self.currency = currency
        self.deribit_messaging = ServiceDeribitMessaging()
        self._end_ts = int(datetime.now().timestamp())*1000
        self._start_ts = int(self._end_ts) - timedelta(hours=1).total_seconds()*1000
        
    @property
    def class_name(self) -> str:
        return f"{self.__class__.__name__}"
    
    @property
    def logger_instance(self):
        return self._logger_instance
    
    @property
    def params(self):
        params = {"resolution":1,
                  "currency": self.currency,
                  "start_timestamp":self._start_ts,
                  "end_timestamp":self._end_ts}
        return params
        
    @property
    def method(self):
        method = "public/get_volatility_index_data"
        return method