import json
from singleton_decorator import singleton

from deribit_arb_app.store.store_observable_order_books import StoreObservableOrderBooks
from deribit_arb_app.converters.converter_json_to_order_book import ConverterJsonToOrderBook

    ####################################################################
    # Service handles Deribit orderbook instances retrived via aiohttp #
    ####################################################################

@singleton
class ServiceDeribitStaticOrderbookHandler():

    def __init__(self):

        self.store_observable_order_books = StoreObservableOrderBooks()
        self.orderbook = None
        
    def set_orderbooks(self, result):

        self.orderbook = ConverterJsonToOrderBook(json.dumps(result)).convert_request_data()
        self.store_observable_order_books.update_observable(self.orderbook)