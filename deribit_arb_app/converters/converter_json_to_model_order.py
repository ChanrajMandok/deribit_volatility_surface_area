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

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[ModelOrder]:

        try:

            if EnumFieldName.RESULT.value not in self.json_obj:
                return None

            json_result = self.json_obj[EnumFieldName.RESULT.value]

            if EnumFieldName.ORDER.value not in json_result:
                return None

            json_order = json_result[EnumFieldName.ORDER.value]

            x = ConverterJsonObjectToModelOrder().convert(json_order)
            return x

        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")
