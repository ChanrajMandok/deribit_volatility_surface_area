from typing import Dict, List, Optional
from singleton_decorator import singleton

from deribit_arb_app.model.model_order import ModelOrder
from deribit_arb_app.model.model_instrument import ModelInstrument

    ##############################################
    # Store Manages & Stores Derebit open orders #
    ##############################################

@singleton
class StoreDeribitOpenOrders():

    # {'BTC': {order_id1: order1, order_id2: order2, ...}, 'ETH': { ... }}

    def __init__(self):
        self.__deribit_open_orders = {}
       
    def get_deribit_open_order(self, instrument: ModelInstrument, order_id: str) -> Optional[ModelOrder]:
        if not instrument.instrument_name in self.__deribit_open_orders.keys():
            return None
        if not order_id in self.__deribit_open_orders[instrument.instrument_name]:
            return None
        return self.__deribit_open_orders[instrument.instrument_name][order_id]

    def set_deribit_open_order(self, order: ModelOrder):
        if not order.instrument_name in self.__deribit_open_orders:
            self.__deribit_open_orders[order.instrument_name] = {}
        self.__deribit_open_orders[order.instrument_name][order.order_id] = order

    def remove_deribit_open_order(self, order: ModelOrder):
        self.__deribit_open_orders[order.instrument_name].pop(order.order_id, None)

    def set_deribit_open_orders(self, deribit_open_orders: Dict[str, Dict[str, ModelOrder]]):
        for instrument_name in deribit_open_orders.keys():
            self.__deribit_open_orders[instrument_name] = deribit_open_orders[instrument_name]   

    def set_deribit_open_orders_list(self, deribit_open_orders_list: List[ModelOrder]) -> Dict[str, Dict[str, ModelOrder]]:
        for order in deribit_open_orders_list:
            if not order.instrument_name in self.__deribit_open_orders:
                self.__deribit_open_orders[order.instrument_name] = {}
            self.__deribit_open_orders[order.instrument_name][order.order_id] = order
        return self.__deribit_open_orders

    def get_deribit_open_orders(self, instrument: ModelInstrument) -> Optional[Dict[str, ModelOrder]]:
        return self.__deribit_open_orders[instrument.instrument_name] if instrument.instrument_name in self.__deribit_open_orders.keys() else None
        