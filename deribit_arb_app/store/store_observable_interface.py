from typing import Mapping, TypeVar, Iterator

from deribit_arb_app.observables.observable_indicator import ObservableIndicator

M = TypeVar('M')
E = TypeVar('E')

    ########################################################
    # Store Observable Manages & Stores observable Objects #
    ########################################################

class StoreObservableInterface(Mapping[E, M]):

    def __init__(self):
        self.d: dict[E, M] = dict()

    def __getitem__(self, item: E) -> M:
        value = str(item)
        return self.d[value]

    def __len__(self) -> int:
        return len(self.d)

    def __iter__(self) -> Iterator[E]:
        return iter(self.d)


    def update_observable(self, observable_instance: M):
        if observable_instance is None:
            return
        
        if not observable_instance.name in self.d:
            self.d[observable_instance.name] = ObservableIndicator(observable_instance)
        self.d[observable_instance.name].set_instance(observable_instance)


    def get_observable(self, observable_instance: M):
        if not observable_instance.name in self.d:
            self.d[observable_instance.name] = ObservableIndicator(observable_instance.__class__(name=observable_instance.name))
        return self.d[observable_instance.name]
    
    
    def remove_observable(self, observable_instance: M):
        if observable_instance.name in self.d:
            del self.d[observable_instance.name]
            

    def remove_observable_by_key(self, key: E):
        if key in self.d:
            del self.d[key]       