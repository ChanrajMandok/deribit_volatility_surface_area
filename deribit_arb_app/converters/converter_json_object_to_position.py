from typing import Optional

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.model.model_position import ModelPosition

    ####################################################
    # Converter Converts Json object to Model Position #
    ####################################################

class ConverterJsonObjectToPosition:

    def __init__(self, json_obj):
        self.json_obj = json_obj

    def convert(self) -> Optional[ModelOrder]:

        try:
            position = ModelPosition(**self.json_obj)
            return position
        except Exception as e:
            raise
