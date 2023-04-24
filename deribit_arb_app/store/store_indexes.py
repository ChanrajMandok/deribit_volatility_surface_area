from typing import List, Optional
from singleton_decorator import singleton

from deribit_arb_app.model.model_index import ModelIndex

    ##########################################
    # Store Manages & Stores Derebit Indexes #
    ##########################################

@singleton
class StoreIndexes:

    def __init__(self):
        self.__deribit_indexes = None

    def set_deribit_indexes(self, indexes: List[ModelIndex]):
        self.__deribit_indexes = indexes

    def get_deribit_indexes(self) -> Optional[List[ModelIndex]]:
        return self.__deribit_indexes
