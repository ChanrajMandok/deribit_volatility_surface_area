import json

from typing import Optional

from deribit_arb_app.converters import logger
from deribit_arb_app.enums.enum_field_name import EnumFieldName

    ###############################################
    # Converter Converts Json object to Heartbeat #
    ###############################################

class ConverterJsonToHeartbeat():
    """
    A converter class to transform a JSON string representing a cancelled order 
    into a ModelOrder instance.
    """

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> Optional[str]:
        """
        Convert the stored JSON object into a ModelOrder instance representing 
        a cancelled order.
        """
        try:
            if EnumFieldName.RESULT.value in self.json_obj:
                return str(self.json_obj[EnumFieldName.RESULT.value])

            if EnumFieldName.PARAMS.value in self.json_obj:
                params = self.json_obj[EnumFieldName.PARAMS.value]

                if EnumFieldName.TYPE.value in params:
                    return str(params[EnumFieldName.TYPE.value])

            return None

        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")