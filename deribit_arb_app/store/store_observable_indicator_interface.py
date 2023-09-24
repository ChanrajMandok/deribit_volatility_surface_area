import sys
import traceback

from typing import Mapping, TypeVar, Iterator

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

        def update_observable(self, observable_indicator_instance: M):
            if observable_indicator_instance is None:
                return 

            if not observable_indicator_instance.key in self.d:
                self.d[observable_indicator_instance.key] = ObservableIndicator(observable_indicator_instance)
            try:
                self.d[observable_indicator_instance.key].set_instance(observable_indicator_instance)
            except Exception as e:
                print(e)
                _, _, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=None, file=None)

        def get_observable(self, observable_indicator_instance: M):
            if not observable_indicator_instance.key in self.d:
                self.d[observable_indicator_instance.key] = ObservableIndicator(observable_indicator_instance)
            return self.d[observable_indicator_instance.key]
        
        def remove_observable(self, observable_indicator_instance: M):
            if observable_indicator_instance is None:
                return

            if observable_indicator_instance.key in self.d:
                del self.d[observable_indicator_instance.key]
                

            