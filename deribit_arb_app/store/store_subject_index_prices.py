from singleton_decorator import singleton

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_index_price import ModelIndexPrice
from deribit_arb_app.subjects.subject_index_price import SubjectIndexPrice

from deribit_arb_app.store.store_subjectable_interface import StoreSubjectableInterface

    #################################################################
    # Store Manages & Stores Subjectable index price Steams objects #
    #################################################################

@singleton
class StoreSubjectIndexPrices(StoreSubjectableInterface):

    def __init__(self):
        self.__subject_index_prices = {}

    def update_subject(self, index_price: ModelIndexPrice):
        if not index_price.index_name in self.__subject_index_prices:
            self.__subject_index_prices[index_price.index_name] = SubjectIndexPrice(index_price)
        self.__subject_index_prices[index_price.index_name].set_instance(index_price)
        # print(f"{index_price.index_name} updated: {index_price.price}")
        
    def get_subject(self, index: ModelIndex) -> SubjectIndexPrice:
        if not index.index_name in self.__subject_index_prices:
            self.__subject_index_prices[index.index_name] = SubjectIndexPrice(ModelIndexPrice(index_name=index.index_name))
        return self.__subject_index_prices[index.index_name]
    
    def remove_subject(self, index: ModelIndex):
        if index.index_name in self.__subject_index_prices:
            del self.__subject_index_prices[index.index_name]
            
    def remove_subject_by_key(self, index_name: str):
        if index_name in self.__subject_index_prices:
            del self.__subject_index_prices[index_name]