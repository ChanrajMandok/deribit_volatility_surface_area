import json

from typing import List

from deribit_arb_app.model.model_index import ModelIndex

    ################################################
    # Converter Converts Json object to ModelIndex #
    ################################################

class ConverterJsonToIndex:

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self)   -> List[ModelIndex]:

        if not "params" in self.json_obj:
            return None

        params = self.json_obj["params"]

        if not "data" in params:
            return None

        data = params["data"]

        index_name = data["index_name"]

        return ModelIndex(
            index_name=index_name
        )
