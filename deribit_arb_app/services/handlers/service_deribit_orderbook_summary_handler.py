import json

from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.converters.converter_json_to_model_orderbook_summary import \
                                              ConverterJsonToModelOrderbookSummary
    
    #############################################
    # Service handles Deribit orderbook summary #
    #############################################

@singleton
class ServiceDeribitOrderbookSummaryHandler():
    """
    Singleton class to manage and handle Deribit orderbook summaries.
    """

    def __init__(self) -> None:
        self.store_subscribable_instruments = Stores.store_subscribable_instruments


    def handle(self, result: dict) -> dict[str, str]:
        """
        Processes and converts the orderbook summary based on the given result.
        """
        orderbook_summary = ConverterJsonToModelOrderbookSummary(json.dumps(result)).convert()  
        return orderbook_summary
