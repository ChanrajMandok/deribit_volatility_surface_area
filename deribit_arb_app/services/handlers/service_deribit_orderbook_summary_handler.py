import json
from typing import Dict
from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.converters.converter_json_to_orderbook_summary_dict import ConverterJsonToOrderbookSummaryDict
    
    #############################################
    # Service handles Deribit orderbook summary #
    #############################################

@singleton
class ServiceDeribitOrderbookSummaryHandler():

    def __init__(self):
        self.store_subscribable_instruments = Stores.store_subscribable_instruments

    def handle(self, result) -> Dict[str, str]:
        orderbook_summary = ConverterJsonToOrderbookSummaryDict(json.dumps(result)).convert()  
        return orderbook_summary