from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_get_interface import \
                                                      ServiceDeribitGetInterface
                                                      
    ################################################################################
    # Service Retrieves Deribit Orderbook Summary by instrument name via Websocket #
    ################################################################################

@singleton
class ServiceDeribitGetOrderbookSummaryInstrument(ServiceDeribitGetInterface):
    """
    Service class to fetch the orderbook summary for a instrument name from Deribit.
    """
    
    def __init__(self,
                 instrument: str) -> None:
        self.instrument = instrument
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
        params = {"instrument_name" : self.instrument,
                  "start_timestamp" : 1599373800000,
                  "end_timestamp" : 1599376800000,
                  "resolution" : "60"}
        return params
        
    @property
    def method(self):
        method = "public/get_book_summary_by_instrument"
        return method