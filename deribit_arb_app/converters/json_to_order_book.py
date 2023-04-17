import json
from typing import Optional

from deribit_arb_app.model.model_order_book import ModelOrderBook


class JsonToOrderBook:

    def __init__(self, json_string):
        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[ModelOrderBook]:

        try:

            if "params" not in self.json_obj:
                return None

            json_obj_params = self.json_obj["params"]

            if "data" not in json_obj_params:
                return None

            json_data = json_obj_params["data"]

            return ModelOrderBook(
                instrument_name=json_data["instrument_name"],
                best_bid_price=json_data["best_bid_price"],
                best_ask_price=json_data["best_ask_price"],
                best_bid_amount=json_data["best_bid_amount"],
                best_ask_amount=json_data["best_ask_amount"]
            )

        except Exception as e:
            raise
