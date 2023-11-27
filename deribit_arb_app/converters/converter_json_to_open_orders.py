import json
import traceback

from typing import Optional

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.enums.enum_field_name import EnumFieldName
from deribit_arb_app.converters.converter_json_object_to_model_order import \
                                              ConverterJsonObjectToModelOrder

    #################################################
    # Converter Converts Json object to Model Order #
    #################################################

class ConverterJsonToOpenOrders:
    """
    Converter class for transforming a JSON string containing open orders into
    a list of ModelOrder instances.
    """
    
    def __init__(self,
                 json_string: str):
        self.json_obj = json.loads(json_string)
        self.json_object_to_order = ConverterJsonObjectToModelOrder()
        
        
    def convert(self) -> Optional[list[ModelOrder]]:
        """
        Converts the internal JSON object into a list of ModelOrder instances.
        """
        orders = []

        try:
            if EnumFieldName.RESULT.value not in self.json_obj:
                return None

            json_orders = self.json_obj[EnumFieldName.RESULT.value]

            for json_order in json_orders:
                order = self.json_object_to_order.convert(json_order)
                orders.append(order)
  
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                      f"Stack trace: {traceback.format_exc()}")

        return orders