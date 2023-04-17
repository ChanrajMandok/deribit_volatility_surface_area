from typing import List, Optional
from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.model.model_index import ModelIndex


@Singleton
class StoreIndexes:

    def __init__(self):
        self.__deribit_indexes = None

    def set_deribit_indexes(self, indexes: List[ModelIndex]):
        self.__deribit_indexes = indexes

    def get_deribit_indexes(self) -> Optional[List[ModelIndex]]:
        return self.__deribit_indexes
