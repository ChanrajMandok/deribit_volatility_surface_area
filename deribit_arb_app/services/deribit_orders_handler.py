from typing import Dict
import json

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.converters.json_to_cancelled_order import JsonToCancelledOrder
from deribit_arb_app.converters.json_to_open_orders import JsonToOpenOrders
from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders
from singleton_pattern_decorator.decorator import Singleton
from deribit_arb_app.converters.json_to_order import JsonToOrder


@Singleton
class DeribitOrdersHandler:

    def __init__(self):
        self.store_deribit_open_orders = StoreDeribitOpenOrders()

    def set_order(self, result) -> ModelOrder:
        order = JsonToOrder(json.dumps(result)).convert()   
        if order.order_state in ["filled", "rejected", "cancelled"]:
            self.store_deribit_open_orders.pop(order.order_id, None)
        else:
            self.store_deribit_open_orders.set_deribit_open_order(order)
        return order
                    
    def set_cancelled_order(self, result) -> ModelOrder:
        order = JsonToCancelledOrder(json.dumps(result)).convert()
        self.store_deribit_open_orders.remove_deribit_open_order(order)
        return order

    def set_open_orders(self, result) -> Dict[str, Dict[str, ModelOrder]]:
        orders = JsonToOpenOrders(json.dumps(result)).convert()
        open_orders_list = self.store_deribit_open_orders.set_deribit_open_orders_list(orders)
        return open_orders_list


