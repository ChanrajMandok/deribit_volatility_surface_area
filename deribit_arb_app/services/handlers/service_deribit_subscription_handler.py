import json
import datetime

from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.converters.converter_json_to_model_observable_order_book import \
                                               ConverterJsonToModelObservableOrderBook
from deribit_arb_app.converters.converter_json_to_model_observable_index_price import \
                                               ConverterJsonToModelObservableIndexPrice
from deribit_arb_app.converters.converter_json_to_model_observable_volatility_index import \
                                             ConverterJsonToModelObservableVolatilityIndex

    #######################################################
    # Service Handles Deribit Subscriptions via Websocket #
    #######################################################

@singleton
class ServiceDeribitSubscriptionHandler():
    """
    Singleton class to manage and handle the subscription operations related to Deribit.

    Attributes:
    - store_observable_order_books: Store for observable order books on Deribit.
    - store_observable_index_prices: Store for observable index prices on Deribit.
    - store_observable_volatility_index: Store for observable volatility index on Deribit.
    """

    def __init__(self) -> None:
        self.store_observable_order_books = Stores.store_observable_orderbooks
        self.store_observable_index_prices = Stores.store_observable_index_prices
        self.store_observable_volatility_index = Stores.store_observable_volatility_index


    def handle(self, 
               result: dict) -> None:
        """
        Handles and processes the subscriptions based on the provided result.
        """
        if "params" not in result:
            return None

        params = result["params"]

        if "channel" not in params:
            return None

        channel = params["channel"]

        if '.' not in channel:
            return None

        if channel.split('.')[0] == "quote":
            order_book = ConverterJsonToModelObservableOrderBook(json.dumps(result)).convert()
            self.store_observable_order_books.update_observable(order_book)

        elif channel.split('.')[0] == "deribit_price_index":
            index_index_price = ConverterJsonToModelObservableIndexPrice(json.dumps(result)).convert()
            self.store_observable_index_prices.update_observable(index_index_price)

        elif channel.split('.')[0] == "deribit_volatility_index":
            volatility_index_value = ConverterJsonToModelObservableVolatilityIndex(json.dumps(result)).convert()
            self.store_observable_volatility_index.update_observable(volatility_index_value)