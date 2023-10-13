import json

from typing import Optional

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_observable_volatility_index import \
                                       ModelObservableVolatilityIndex

    ####################################################################
    # Converter Converts Json object to ModelObservableVolatilityIndex #
    ####################################################################

class ConverterJsonToModelObservableVolatilityIndex():
    """
    A converter class that transforms a JSON string to an instance
    of ModelObservableVolatilityIndex.
    
    The purpose of this class is to extract relevant information
    from a provided JSON string and use it to instantiate and return
    a ModelObservableVolatilityIndex object.
    """
    
    def __init__(self, json_string: str):
        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[ModelObservableVolatilityIndex]:
        """
        Converts the loaded JSON object to a ModelObservableVolatilityIndex instance.
        
        The method navigates through the nested structure of the JSON object and
        extracts the required information to instantiate a ModelObservableVolatilityIndex object.
        If the required fields are missing in the JSON object, it returns None.
        """
        try:
            # Check if the JSON object has 'params' key, if not return None.
            if "params" not in self.json_obj:
                return None
            
            json_obj_params = self.json_obj["params"]
            
            # Check if 'params' has 'data' key, if not return None.
            if "data" not in json_obj_params:
                return None

            json_data = json_obj_params["data"]
            
            # Extract values from 'data' and create a ModelObservableVolatilityIndex instance.
            volatility_index = ModelObservableVolatilityIndex(
                                                              name=json_data["index_name"],
                                                              timestamp=json_data['timestamp'],
                                                              volatility=json_data['volatility']
                                                             )
            
            # Return the created ModelObservableVolatilityIndex instance.
            return volatility_index

        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")