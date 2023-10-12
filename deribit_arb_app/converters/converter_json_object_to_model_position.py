from typing import Optional

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.model.model_position import ModelPosition

    ####################################################
    # Converter Converts Json object to Model Position #
    ####################################################

class ConverterJsonObjectToModelPosition():
    """
    A converter class to transform a JSON object into a ModelPosition instance.
    """

    def __init__(self, json_obj):
        self.json_obj = json_obj

    def convert(self) -> Optional[ModelOrder]: 
        """
        Converts the stored JSON object into a ModelPosition instance.
        """
        
        try:
            position = ModelPosition(**self.json_obj)
            return position
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")