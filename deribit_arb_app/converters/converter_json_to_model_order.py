import json

from typing import Optional

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.enums.enum_field_name import EnumFieldName
from deribit_arb_app.converters.converter_json_object_to_model_order import \
                                              ConverterJsonObjectToModelOrder

    ################################################
    # Converter Converts Json object to ModelOrder #
    ################################################

class ConverterJsonToModelOrder():
    """ Converter class to transform a JSON string into a ModelOrder instance."""
        
    def __init__(self, json_string: str):
        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[ModelOrder]:
        """ Converts the internal JSON object into a ModelOrder instance."""
        try:
            # Check if the 'RESULT' field is in the JSON object
            if EnumFieldName.RESULT.value not in self.json_obj:
                return None

            json_result = self.json_obj[EnumFieldName.RESULT.value]

            # Check if the 'ORDER' field is in the 'RESULT' section of the JSON object
            if EnumFieldName.ORDER.value not in json_result:
                return None

            json_order = json_result[EnumFieldName.ORDER.value]

            # Use another converter to transform the 'ORDER' section into a ModelOrder instance
            x = ConverterJsonObjectToModelOrder().convert(json_order)
            return x

        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")
