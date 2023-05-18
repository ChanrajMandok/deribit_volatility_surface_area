import json

from singleton_decorator import singleton
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.converters.converter_json_to_order_book import ConverterJsonToOrderBook

    ####################################################################
    # Service handles Deribit orderbook instances retrived via aiohttp #
    ####################################################################

@singleton
class ServiceDeribitStaticOrderbookHandler():

    def __init__(self):

        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.orderbook = None
        
    def set_orderbooks(self, result):

        self.orderbook = ConverterJsonToOrderBook(json.dumps(result)).convert_request_data()
        self.store_subject_order_books.update_subject(self.orderbook)