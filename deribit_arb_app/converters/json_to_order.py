import json
from typing import Optional

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.enums.field_name import FieldName

from deribit_arb_app.converters.json_object_to_order import JsonObjectToOrder


class JsonToOrder:

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[ModelOrder]:

        try:

            if FieldName.RESULT.value not in self.json_obj:
                return None

            json_result = self.json_obj[FieldName.RESULT.value]

            if FieldName.ORDER.value not in json_result:
                return None

            json_order = json_result[FieldName.ORDER.value]

            return JsonObjectToOrder().convert(json_order)

        except Exception as e:
            raise
