import json
from singleton_decorator import singleton

from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.converters.converter_json_to_order_book import ConverterJsonToOrderBook
from deribit_arb_app.converters.converter_json_to_index_price import ConverterJsonToIndexPrice

    #######################################################
    # Service Handles Deribit Subscriptions via Websocket #
    #######################################################

@singleton
class ServiceDeribitSubscriptionHandler:

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
            
            self.order_book = ConverterJsonToOrderBook(json.dumps(result)).convert()
            self.store_subject_order_books.update_subject(self.order_book)

        elif channel.split('.')[0] == "deribit_price_index":
            
            self.index_index_price = ConverterJsonToIndexPrice(json.dumps(result)).convert()
            self.store_subject_index_prices.update_subject(self.index_index_price)
