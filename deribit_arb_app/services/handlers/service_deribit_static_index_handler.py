import json

from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.converters.converter_json_to_model_observable_index_price import \
                                               ConverterJsonToModelObservableIndexPrice
from deribit_arb_app.converters.converter_json_to_model_observable_volatility_index import \
                                               ConverterJsonToModelObservableVolatilityIndex
                                               

    ####################################################################
    # Service handles Deribit orderbook instances retrived via aiohttp #
    ####################################################################

@singleton
class ServiceDeribitStaticIndexHandler():
    """
    Singleton class to manage and handle the static order book operations 
    related to Deribit.
    """

    def __init__(self) -> None:
        self.store_observable_index_prices = Stores.store_observable_index_prices
        self.store_observable_volatility_index = Stores.store_observable_volatility_index
        self.orderbook = None


    def set(self, result: dict) -> None:
        """
        Processes and sets the order books based on the provided result.
        """
        if result['method'] == '':
            self.index_object = ConverterJsonToModelObservableIndexPrice(json.dumps(result)).convert_request_data()
            self.store_observable_index_prices.update(self.orderbook)
        if result['method'] == '':
            pass