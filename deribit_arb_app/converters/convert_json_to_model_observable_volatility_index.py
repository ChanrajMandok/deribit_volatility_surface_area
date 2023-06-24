import json
from typing import Optional

from deribit_arb_app.model.model_observable_volatility_index import ModelObservableVolatilityIndex

    ####################################################################
    # Converter Converts Json object to ModelObservableVolatilityIndex #
    ####################################################################

class ConverterJsonToModelObservableVolatilityIndex():

    def __init__(self, json_string):
        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[ModelObservableVolatilityIndex]:

        try:

            if "params" not in self.json_obj:
                return None

            json_obj_params = self.json_obj["params"]

            if "data" not in json_obj_params:
                return None

            json_data = json_obj_params["data"]

            volatility_index =   ModelObservableVolatilityIndex(
                                        name = json_data["index_name"],
                                        timestamp = json_data['timestamp'],
                                        volatility = json_data['volatility']
                                        )
            
            return volatility_index

        except Exception as e:
            raise
