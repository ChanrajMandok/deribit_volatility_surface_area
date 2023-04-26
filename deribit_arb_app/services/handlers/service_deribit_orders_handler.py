import json
from typing import Dict

from singleton_decorator import singleton
from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders

from deribit_arb_app.converters.converter_json_to_order import ConverterJsonToOrder
from deribit_arb_app.converters.converter_json_to_open_orders import ConverterJsonToOpenOrders
from deribit_arb_app.converters.converter_json_to_cancelled_order import ConverterJsonToCancelledOrder

    ##################################
    # Service Handles Deribit orders #
    ##################################

@singleton
class ServiceDeribitOrdersHandler:

    def __init__(self):
        self.store_deribit_open_orders = StoreDeribitOpenOrders()

    def set_order(self, result) -> ModelOrder:
        order = ConverterJsonToOrder(json.dumps(result)).convert()   
        if order.order_state in ["filled", "rejected", "cancelled"]:
            self.store_deribit_open_orders.pop(order.order_id, None)
        else:
            self.store_deribit_open_orders.set_deribit_open_order(order)
        return order
                    
    def set_cancelled_order(self, result) -> ModelOrder:
        order = ConverterJsonToCancelledOrder(json.dumps(result)).convert()
        self.store_deribit_open_orders.remove_deribit_open_order(order)
        return order

    def set_open_orders(self, result) -> Dict[str, Dict[str, ModelOrder]]:
        orders = ConverterJsonToOpenOrders(json.dumps(result)).convert()
        open_orders_list = self.store_deribit_open_orders.set_deribit_open_orders_list(orders)
        return open_orders_list


