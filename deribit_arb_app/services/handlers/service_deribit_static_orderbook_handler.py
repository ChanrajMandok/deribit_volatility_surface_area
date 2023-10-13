import json

from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.converters.converter_json_to_model_observable_order_book import \
                                               ConverterJsonToModelObservableOrderBook
                                               
    ####################################################################
    # Service handles Deribit orderbook instances retrived via aiohttp #
    ####################################################################

from singleton_decorator import singleton

@singleton
class ServiceDeribitStaticOrderbookHandler():
    """
    Singleton class to manage and handle the static order book operations 
    related to Deribit.
    """

    def __init__(self) -> None:
        self.store_observable_order_books = Stores.store_observable_orderbooks
        self.orderbook = None

    def set_orderbooks(self, result: dict) -> None:
        """
        Processes and sets the order books based on the provided result.
        """
        self.orderbook = ConverterJsonToModelObservableOrderBook(json.dumps(result)).convert_request_data()
        self.store_observable_order_books.update_observable(self.orderbook)