import json

from singleton_decorator import singleton

from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders

    ###########################################################
    # Service handles Operations after Cancelling all Orders  #
    ###########################################################

from singleton_decorator import singleton


@singleton
class ServiceDeribitCancelAllPositionsHandler():
    """
    Singleton class to manage and handle the cancellation of all Deribit positions.
    """

    def __init__(self) -> None:
        self.store_deribit_open_orders = StoreDeribitOpenOrders()


    def cancel_all(self, result: dict) -> None:
        """
        Processes the cancellation of all positions based on the given result.
        If the number of open orders matches the result, all positions are cancelled.
        """
        positions_closed = int(result['result']) if result['result'] else None
        if positions_closed == self.store_deribit_open_orders.__len__():
            self.store_deribit_open_orders.clear_store()
