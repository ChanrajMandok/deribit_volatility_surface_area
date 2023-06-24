import json

from typing import Optional

from deribit_arb_app.model.model_observable_index_price import ModelObservableIndexPrice

    #####################################################
    # Converter Converts Json object to ModelIndexPrice #
    #####################################################

class ConverterJsonToModelObservableIndexPrice():

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self)  -> Optional[ModelObservableIndexPrice]:

        if not "params" in self.json_obj:
             return None

        params = self.json_obj["params"]

        if not "data" in params:
            return None

        data = params["data"]

        index_name   = data["index_name"]
        price        = data["price"]
        timestamp    = data["timestamp"]

        return ModelObservableIndexPrice(
            name        =index_name,
            price       =price,
            timestamp   =timestamp
        )
