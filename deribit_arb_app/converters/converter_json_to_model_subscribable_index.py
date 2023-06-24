import json

from typing import List

from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex

    ################################################
    # Converter Converts Json object to ModelIndex #
    ################################################

class ConverterJsonToModelSubscribableIndex():

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> List[ModelSubscribableIndex]:

        if not "params" in self.json_obj:
            return None

        params     = self.json_obj["params"]

        if not "data" in params:
            return None

        data       = params["data"]

        index_name = data["index_name"]

        return ModelSubscribableIndex(
            name  = index_name
        )
