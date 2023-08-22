import json
from typing import List, Optional

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.enums.enum_field_name import EnumFieldName

from deribit_arb_app.converters.converter_json_object_to_model_order import ConverterJsonObjectToModelOrder

    #################################################
    # Converter Converts Json object to Model Order #
    #################################################

class ConverterJsonToOpenOrders():

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)
        self.json_object_to_order = ConverterJsonObjectToModelOrder()
        
    def convert(self) -> Optional[List[ModelOrder]]:

        orders = []

        try:

            if EnumFieldName.RESULT.value not in self.json_obj:
                return None

            json_orders = self.json_obj[EnumFieldName.RESULT.value]

            for json_order in json_orders:

                order = self.json_object_to_order.convert(json_order)
                orders.append(order)
  
        except Exception as e:
            raise Exception(f"{self.__class__.__name__}: {e}")

        return orders
