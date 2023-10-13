import json

from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex

    ################################################
    # Converter Converts Json object to ModelIndex #
    ################################################

class ConverterJsonToModelSubscribableIndex():
    """
    Converter class to transform a JSON string into a ModelSubscribableIndex
    instance.
    """

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> list[ModelSubscribableIndex]:
        """Converts the internal JSON object into a ModelSubscribableIndex instance."""

        if not "params" in self.json_obj:
            return None

        params = self.json_obj["params"]

        if not "data" in params:
            return None

        data = params["data"]

        index_name = data["index_name"]

        model_subscribable_index = \
            ModelSubscribableIndex(name=index_name)
        
        return model_subscribable_index