import json
from typing import Optional

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_observable_order_book import ModelObservableOrderBook

    ####################################################
    # Converter Converts Json object to ModelOrderBook #
    ####################################################

class ConverterJsonToModelObservableOrderBook():
    """
    Converter class that transforms a JSON string  into a `ModelObservableOrderBook` instance.
    """
    
    def __init__(self, json_string):
        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[ModelObservableOrderBook]:
        """
        Parses the stored JSON object and converts it into a ModelObservableOrderBook instance. 
        If necessary fields (`params` or `data`) are missing, it returns `None`.
        """
        try:
            if "params" not in self.json_obj:
                return None

            json_obj_params = self.json_obj["params"]

            if "data" not in json_obj_params:
                return None

            json_data = json_obj_params["data"]

            orderbook =  \
                ModelObservableOrderBook(
                                         name              = json_data["instrument_name"],
                                         best_bid_price    = json_data["best_bid_price"],
                                         best_ask_price    = json_data["best_ask_price"],
                                         best_bid_amount   = json_data["best_bid_amount"],
                                         best_ask_amount   = json_data["best_ask_amount"]
                                         )
            
            return orderbook

        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")


    def convert_request_data(self) -> Optional[ModelObservableOrderBook]:
        """
        Converts the stored JSON object into a ModelObservableOrderBook instance, assuming it 
        directly contains the 'data' format fields without the need to navigate to the 'params' section.
        """
        try:
            json_data = self.json_obj

            orderbook =  \
                ModelObservableOrderBook(
                                        name              = json_data["instrument_name"],
                                        best_bid_price    = json_data["best_bid_price"],
                                        best_ask_price    = json_data["best_ask_price"],
                                        best_bid_amount   = json_data["best_bid_amount"],
                                        best_ask_amount   = json_data["best_ask_amount"]
                                        )
                
            return orderbook
        
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")