import json
from singleton_decorator import singleton

from deribit_arb_app.store.store_observable_order_books import StoreObservableOrderBooks
from deribit_arb_app.store.store_observable_index_prices import StoreObservableIndexPrices
from deribit_arb_app.converters.converter_json_to_order_book import ConverterJsonToOrderBook
from deribit_arb_app.converters.converter_json_to_index_price import ConverterJsonToIndexPrice

    #######################################################
    # Service Handles Deribit Subscriptions via Websocket #
    #######################################################

@singleton
class ServiceDeribitSubscriptionHandler():

    def __init__(self):
        self.store_observable_order_books = StoreObservableOrderBooks()
        self.store_observable_index_prices = StoreObservableIndexPrices()

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
            self.store_observable_order_books.update_observable(self.order_book)

        elif channel.split('.')[0] == "deribit_price_index":
            
            self.index_index_price = ConverterJsonToIndexPrice(json.dumps(result)).convert()
            self.store_observable_index_prices.update_observable(self.index_index_price)
