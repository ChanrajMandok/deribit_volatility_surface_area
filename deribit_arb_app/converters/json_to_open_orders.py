import json
from typing import List, Optional

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.enums.field_name import FieldName

from deribit_arb_app.converters.json_object_to_order import JsonObjectToOrder


class JsonToOpenOrders:

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)
        self.json_object_to_order = JsonObjectToOrder()
        
    def convert(self) -> Optional[List[ModelOrder]]:

        orders = []

        try:

            if FieldName.RESULT.value not in self.json_obj:
                return None

            json_orders = self.json_obj[FieldName.RESULT.value]

            for json_order in json_orders:

                order = self.json_object_to_order.convert(json_order)
                orders.append(order)
  
        except Exception as e:
            raise

        return orders
