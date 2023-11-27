import json

from singleton_decorator import singleton

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.store.store_deribit_open_orders import \
                                       StoreDeribitOpenOrders
from deribit_arb_app.converters.converter_json_to_model_order import \
                                             ConverterJsonToModelOrder
from deribit_arb_app.converters.converter_json_to_open_orders import \
                                             ConverterJsonToOpenOrders
from deribit_arb_app.converters.converter_json_to_cancelled_order import \
                                             ConverterJsonToCancelledOrder
                                             
    ##################################
    # Service Handles Deribit orders #
    ##################################

from singleton_decorator import singleton

@singleton
class ServiceDeribitOrdersHandler():
    """
    Singleton class responsible for handling the state and operations
    of Deribit orders.
    """
    
    def __init__(self) -> None:
        self.store_deribit_open_orders = StoreDeribitOpenOrders()


    def set_order(self, result: dict) -> ModelOrder:
        """
        Processes, converts, and sets the order based on the given result.
        """
        order = ConverterJsonToModelOrder(json.dumps(result)).convert()   
        if order.order_state in ["filled", "rejected", "cancelled"]:
            self.store_deribit_open_orders.pop(order.order_id, None)
        else:
            self.store_deribit_open_orders.set_deribit_open_order(order)
        return order


    def set_cancelled_order(self, result: dict) -> ModelOrder:
        """
        Processes, converts, and removes the cancelled order from the store.
        """
        order = ConverterJsonToCancelledOrder(json.dumps(result)).convert()
        self.store_deribit_open_orders.remove_deribit_open_order(order)
        return order


    def set_open_orders(self, result: dict) -> dict[str, dict[str, ModelOrder]]:
        """
        Processes, converts, and sets the open orders list based on the given result.
        """
        orders = ConverterJsonToOpenOrders(json.dumps(result)).convert()
        open_orders_list = self.store_deribit_open_orders.set_deribit_open_orders_list(orders)
        return open_orders_list