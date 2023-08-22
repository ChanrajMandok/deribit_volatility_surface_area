import json
from typing import Optional

from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.enums.enum_field_name import EnumFieldName

from deribit_arb_app.converters.converter_json_object_to_model_position import ConverterJsonObjectToModelPosition

    ###################################################
    # Converter Converts Json object to ModelPosition #
    ###################################################

class ConverterJsonToModelPositions():
    
    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[ModelPosition]:

        positions = []

        try:

            if EnumFieldName.RESULT.value not in self.json_obj:
                return None

            json_result = self.json_obj[EnumFieldName.RESULT.value]
            
            for position_json in json_result:
                position = ConverterJsonObjectToModelPosition(position_json).convert()
                positions.append(position)

            return positions

        except Exception as e:
            raise Exception(f"{self.__class__.__name__}: {e}")