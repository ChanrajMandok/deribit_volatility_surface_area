from singleton_decorator import singleton

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.observables.observable_indicator import ObservableIndicator
from deribit_arb_app.model.model_index_price import ModelIndexPrice
from deribit_arb_app.store.store_observable_interface import StoreObservableInterface

    #################################################################
    # Store Manages & Stores Observable index price Steams objects #
    #################################################################

@singleton
class StoreObservableIndexPrices(StoreObservableInterface):

    def __init__(self):
        self.__observable_index_prices = {}

    def update_observable(self, index_price: ModelIndexPrice):
        if not index_price.index_name in self.__observable_index_prices:
            self.__observable_index_prices[index_price.index_name] = ObservableIndicator(index_price)
        self.__observable_index_prices[index_price.index_name].set_instance(index_price)
        print(f"{index_price.index_name} updated: {index_price.price}")
        
    def get_observable(self, index: ModelIndex):
        if not index.index_name in self.__observable_index_prices:
            self.__observable_index_prices[index.index_name] = ObservableIndicator(ModelIndexPrice(index_name=index.index_name))
        return self.__observable_index_prices[index.index_name]
    
    def remove_observable(self, index: ModelIndex):
        if index.index_name in self.__observable_index_prices:
            del self.__observable_index_prices[index.index_name]
            
    def remove_observable_by_key(self, index_name: str):
        if index_name in self.__observable_index_prices:
            del self.__observable_index_prices[index_name]