import json
from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.converters.json_to_order_book import JsonToOrderBook
from deribit_arb_app.converters.json_to_index_price import JsonToIndexPrice


@Singleton
class DeribitSubscriptionHandler:

    def __init__(self):
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.store_subject_index_prices = StoreSubjectIndexPrices()

    def handle(self, result):

        if not "params" in result:
            return None

        params = result["params"]

        if not "channel" in params:
            return None

        channel = params["channel"]

        if not '.' in channel:
            return None

        if channel.split('.')[0] == "quote":
            
            self.order_book = JsonToOrderBook(json.dumps(result)).convert()
            self.store_subject_order_books.update_subject(self.order_book)

        elif channel.split('.')[0] == "deribit_price_index":
            
            self.index_index_price = JsonToIndexPrice(json.dumps(result)).convert()
            self.store_subject_index_prices.update_subject(self.index_index_price)
