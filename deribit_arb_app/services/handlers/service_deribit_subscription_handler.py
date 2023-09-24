import json

from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.converters.converter_json_to_model_observable_order_book import \
                                               ConverterJsonToModelObservableOrderBook
from deribit_arb_app.converters.converter_json_to_model_observable_index_price import \
                                               ConverterJsonToModelObservableIndexPrice
from deribit_arb_app.converters.convert_json_to_model_observable_volatility_index import \
                                             ConverterJsonToModelObservableVolatilityIndex

    #######################################################
    # Service Handles Deribit Subscriptions via Websocket #
    #######################################################

@singleton
class ServiceDeribitSubscriptionHandler():

    def __init__(self):
        self.store_observable_order_books       = Stores.store_observable_orderbooks
        self.store_observable_index_prices      = Stores.store_observable_index_prices
        self.store_observable_volatility_index  = Stores.store_observable_volatility_index

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
            
            self.order_book = ConverterJsonToModelObservableOrderBook(json.dumps(result)).convert()
            self.store_observable_order_books.update_observable(self.order_book)

        elif channel.split('.')[0] == "deribit_price_index":
            
            self.index_index_price = ConverterJsonToModelObservableIndexPrice(json.dumps(result)).convert()
            self.store_observable_index_prices.update_observable(self.index_index_price)
            
        elif channel.split('.')[0] == "deribit_volatility_index":
            self.volatility_index_value = ConverterJsonToModelObservableVolatilityIndex(json.dumps(result)).convert()
            self.store_observable_volatility_index.update_observable(self.volatility_index_value)