import json 
import traceback

from typing import Optional

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.enums.enum_field_name import EnumFieldName
from deribit_arb_app.converters.converter_json_object_to_model_order import \
                                              ConverterJsonObjectToModelOrder

    ################################################
    # Converter Converts Json object to ModelOrder #
    ################################################

class ConverterJsonToCancelledOrder():
    """
    Converter class that transforms a JSON string representation 
    of a cancelled order into a `ModelOrder` instance.
    """

    def __init__(self,
                 json_string):
        self.json_obj = json.loads(json_string)


    def convert(self) -> Optional[ModelOrder]:
        """
        Converts the stored JSON object into a ModelOrder instance.
        Checks if the necessary fields (`EnumFieldName.RESULT.value`) 
        are present in the JSON before conversion.
        """
        try:
            if EnumFieldName.RESULT.value not in self.json_obj:
                return None

            json_result = self.json_obj[EnumFieldName.RESULT.value]
            return ConverterJsonObjectToModelOrder().convert(json_result)

        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                      f"Stack trace: {traceback.format_exc()}")