from typing import Mapping, TypeVar, Optional, Iterator

M = TypeVar('M')
E = TypeVar('E')

    ###############################################################
    # Store interface Manages & Stores Model Subscribable Objects #
    ###############################################################

class StoreSubscribableInterface(Mapping[E, M]):

    def __init__(self):
        self.d: dict[E, M] = dict()

    def __getitem__(self, item: E) -> M:
        value = str(item)
        return self.d[value]

    def __len__(self) -> int:
        return len(self.d)

    def __iter__(self) -> Iterator[E]:
        return iter(self.d)
        
    def set_subscribables(self, model_subscribable_instance_list: list[M]):
        for subscribable in model_subscribable_instance_list:
            if not subscribable.name in self.d:
                self.d[subscribable.name] = None
            self.d[subscribable.name] = subscribable

    def get_subscribables(self) -> dict[E, M]:
        return self.d

    def get_subscribable_via_key(self, key: E) -> Optional[M]:
        return self.d[key]
    
    


