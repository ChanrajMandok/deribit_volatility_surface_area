import json

from typing import Optional

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_position import ModelPosition
from deribit_arb_app.enums.enum_field_name import EnumFieldName
from deribit_arb_app.converters.converter_json_object_to_model_position import \
                                              ConverterJsonObjectToModelPosition

    ###################################################
    # Converter Converts Json object to ModelPosition #
    ###################################################

class ConverterJsonToModelPositions:
    """
    Converter class to transform a JSON string representing positions into a list 
    of ModelPosition instances.
    """
    
    def __init__(self, json_string: str):
        """Initialize the converter with the given JSON string."""

        try:
            self.json_obj = json.loads(json_string)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON string provided to {self.__class__.__name__}.")
            self.json_obj = None

    def convert(self) -> Optional[list[ModelPosition]]:
        """
        Converts the internal JSON object into a list of ModelPosition instances.
        """

        positions = []

        if not self.json_obj:
            return None

        try:
            json_result = self.json_obj.get(EnumFieldName.RESULT.value, [])

            if not isinstance(json_result, list):
                logger.warning("Expected a list of positions in the 'result' field.")
                return None
            
            for position_json in json_result:
                converter = ConverterJsonObjectToModelPosition(position_json)
                position = converter.convert()
                if position:
                    positions.append(position)

            return positions

        except Exception as e:
            logger.error(f"An error occurred during conversion in {self.__class__.__name__}: {e}")
            return None