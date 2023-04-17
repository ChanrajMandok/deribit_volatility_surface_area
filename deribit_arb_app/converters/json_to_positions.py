import json
from typing import Optional

from deribit_arb_app.converters.json_object_to_position import JsonObjectToPosition
from deribit_arb_app.enums.field_name import FieldName
from deribit_arb_app.model.model_position import ModelPosition


class JsonToPositions:
    
    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[ModelPosition]:

        positions = []

        try:

            if FieldName.RESULT.value not in self.json_obj:
                return None

            json_result = self.json_obj[FieldName.RESULT.value]

            for position_json in json_result:
                position = JsonObjectToPosition(position_json).convert()
                positions.append(position)

            return positions

        except Exception as e:
            raise