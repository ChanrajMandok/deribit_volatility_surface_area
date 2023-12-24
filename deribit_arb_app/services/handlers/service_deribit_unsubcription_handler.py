from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores

    #########################################################
    # Service Handles Deribit Unsubscriptions via Websocket #
    #########################################################

@singleton
class ServiceDeribitUnsubscriptionHandler():
    """
    Singleton class to manage and handle unsubscription operations related to Deribit.
    """

    def __init__(self) -> None:
        self.store_observable_order_books = Stores.store_observable_orderbooks
        self.store_observable_index_prices = Stores.store_observable_index_prices


    def handle(self, result: dict) -> None:
        """
        Processes the provided result to handle unsubscription and remove observables based on channel types.
        """
        if "result" not in result:
            return None

        params = result["result"]

        for unsub_channel in params:
            if '.' not in unsub_channel:
                return None

            channel_type = unsub_channel.split('.')[0]
            key = unsub_channel.split('.')[1]

            if channel_type == "quote":
                self.store_observable_order_books.remove_by_key(key)

            elif channel_type == "deribit_price_index":
                self.store_observable_index_prices.remove_by_key(key)
