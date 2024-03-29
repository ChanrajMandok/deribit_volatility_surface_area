import traceback

from typing import Mapping, TypeVar, Iterator

from deribit_arb_app.store import logger
from deribit_arb_app.observables.observable_indicator import ObservableIndicator

M = TypeVar('M')
E = TypeVar('E')

    ######################################################################################
    # Store Observable Indicator Interface Stores & Manages Observable Indicator Objects #
    ######################################################################################

class StoreObservableIndicatorInterface(Mapping[E, M]):

        def __init__(self):
            self.d: dict[E, M] = dict()


        def __getitem__(self, item: E) -> M:
            value = str(item)
            return self.d[value]


        def __len__(self) -> int:
            return len(self.d)


        def __iter__(self) -> Iterator[E]:
            return iter(self.d)


        def update(self, observable_indicator_instance: M):
            if observable_indicator_instance is None:
                return 

            if not observable_indicator_instance.key in self.d:
                self.d[observable_indicator_instance.key] = ObservableIndicator(observable_indicator_instance)
            try:
                self.d[observable_indicator_instance.key].set_instance(observable_indicator_instance)
            except Exception as e:
                        logger.error(f"{self.__class__.__name__}: Error: {str(e)}. Stack trace: {traceback.format_exc()}")
                

        def get(self, observable_indicator_instance: M):
            if not observable_indicator_instance.key in self.d:
                self.d[observable_indicator_instance.key] = ObservableIndicator(observable_indicator_instance)
            return self.d[observable_indicator_instance.key]
        
        
        def remove(self, observable_indicator_instance: M):
            if observable_indicator_instance is None:
                return

            if observable_indicator_instance.key in self.d:
                del self.d[observable_indicator_instance.key]