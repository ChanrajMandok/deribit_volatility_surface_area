import json

from typing import Optional

from deribit_arb_app.converters import logger
from deribit_arb_app.enums.enum_field_name import EnumFieldName

    ############################################
    # Converter Converts Json object to String #
    ############################################

class ConverterJsonToTestResponse():

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[str]:

        try:

            if EnumFieldName.RESULT.value in self.json_obj:
                return str(self.json_obj[EnumFieldName.RESULT.value])

            if EnumFieldName.VERSION.value in self.json_obj:
                params = self.json_obj[EnumFieldName.PARAMS.value]

                if EnumFieldName.TYPE.value in params:
                    return str(type)

            return None
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")
