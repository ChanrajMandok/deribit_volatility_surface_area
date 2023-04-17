import json
from typing import Optional

from deribit_arb_app.enums.field_name import FieldName


class JsonToHeartbeat:

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[str]:

        try:

            if FieldName.RESULT.value in self.json_obj:
                return str(self.json_obj[FieldName.RESULT.value])

            if FieldName.PARAMS.value in self.json_obj:
                params = self.json_obj[FieldName.PARAMS.value]

                if FieldName.TYPE.value in params:
                    return str(params[FieldName.TYPE.value])

            return None

        except Exception as e:
            raise
