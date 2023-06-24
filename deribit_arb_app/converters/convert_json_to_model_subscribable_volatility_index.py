import json

from typing import List

from deribit_arb_app.model.model_subscribable_volatility_index import ModelSubscribableVolatilityIndex

    ######################################################################
    # Converter Converts Json object to ModelSubscribableVolatilityIndex #
    ######################################################################

class ConverterJsonToModelSubscribableVolatilityIndex():

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> List[ModelSubscribableVolatilityIndex]:

        if not "params" in self.json_obj:
            return None

        params     = self.json_obj["params"]

        if not "data" in params:
            return None

        data       = params["data"]

        index_name   = data["index_name"]

        return ModelSubscribableVolatilityIndex(
            name = index_name,
        )
