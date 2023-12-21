import json
import traceback

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_subscribable_volatility_index import \
                                        ModelSubscribableVolatilityIndex

    ######################################################################
    # Converter Converts Json object to ModelSubscribableVolatilityIndex #
    ######################################################################

class ConverterJsonToModelSubscribableVolatilityIndex():
    """
    A converter class that is responsible for converting a JSON string to a 
    ModelSubscribableVolatilityIndex object.
    """
    
    def __init__(self,
                 json_string: str):
        self.json_obj = json.loads(json_string)


    def convert(self) -> ModelSubscribableVolatilityIndex:
        """
        Converts the JSON object to a ModelSubscribableVolatilityIndex object.
        """
        try:
            if not "params" in self.json_obj:
                return None
            
            params = self.json_obj["params"]
            
            if not "data" in params:
                return None
            
            data = params["data"]
            
            index_name = data["index_name"]
            
            model_subscribable_volatility_index =\
                          ModelSubscribableVolatilityIndex(name=index_name) 
            
            return model_subscribable_volatility_index
        
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                      f"Stack trace: {traceback.format_exc()}")