import json

from typing import Optional

from deribit_arb_app.model.model_observable_index_price import \
                                        ModelObservableIndexPrice

    #####################################################
    # Converter Converts Json object to ModelIndexPrice #
    #####################################################

class ConverterJsonToModelObservableIndexPrice():
    """
    Converter class that transforms a JSON string representation 
    into a `ModelObservableIndexPrice` instance.
    """
    
    def __init__(self,
                 json_string):
        self.json_obj = json.loads(json_string)


    def convert(self)  -> Optional[ModelObservableIndexPrice]:
        """
        Converts the stored JSON object into a ModelObservableIndexPrice instance.
        If the necessary fields (`params`) are absent in the JSON, it returns `None`.
        """
        
        if not "params" in self.json_obj:
             return None

        params = self.json_obj["params"]

        if not "data" in params:
            return None

        data = params["data"]

        price        = data["price"]
        timestamp    = data["timestamp"]
        index_name   = data["index_name"]

        model_observable_price = \
              ModelObservableIndexPrice(
                                        price       =price,
                                        timestamp   =timestamp,
                                        name        =index_name,
                                        )
        
        return model_observable_price