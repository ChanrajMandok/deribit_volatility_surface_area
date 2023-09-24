import json

from singleton_decorator import singleton

from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders

    ###########################################################
    # Service handles Operations after Cancelling all Orders  #
    ###########################################################

@singleton
class ServiceDeribitCancelAllPositionsHandler():

    def __init__(self):
        self.store_deribit_open_orders = StoreDeribitOpenOrders()

    def cancel_all(self, result) -> None:
        positions_closed = int(result['result']) if result['result'] else None 
        if self.store_deribit_open_orders.__len__() ==  result:
            self.store_deribit_open_orders.clear_store()