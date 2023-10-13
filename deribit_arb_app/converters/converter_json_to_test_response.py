import json

from typing import Optional

from deribit_arb_app.converters import logger
from deribit_arb_app.enums.enum_field_name import EnumFieldName

    ############################################
    # Converter Converts Json object to String #
    ############################################

class ConverterJsonToTestResponse:
    """
    Converter class to transform a JSON string into a test response.
    """
    
    def __init__(self, json_string: str):
        try:
            self.json_obj = json.loads(json_string)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON string provided to {self.__class__.__name__}.")
            self.json_obj = None

    def convert(self) -> Optional[str]:
        """Converts the internal JSON object into a test response string."""

        try:
            # Check if RESULT field exists in json_obj
            if EnumFieldName.RESULT.value in self.json_obj:
                return str(self.json_obj[EnumFieldName.RESULT.value])
            
            # Check if VERSION field exists in json_obj
            if EnumFieldName.VERSION.value in self.json_obj:
                params = self.json_obj.get(EnumFieldName.PARAMS.value, {})
                if EnumFieldName.TYPE.value in params:
                    return str(params[EnumFieldName.TYPE.value])
            
            return None

        except Exception as e:
            logger.error(f"An error occurred during conversion in {self.__class__.__name__}: {e}")
            return None