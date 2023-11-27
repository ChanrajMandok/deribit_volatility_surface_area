from abc import ABC, abstractmethod
from typing import Iterator, Mapping, TypeVar

    ##################################################
    # Interface provides observers with update logic #
    ##################################################

E=TypeVar('E')
M=TypeVar('M')

class ObserverInterface(ABC, Mapping[E, M]):
    """
    The Observer interface declares the update method, used by observable
    """


    def update(self, key: E, instance: M, old_instance: M, change: object) -> None:
        """
        Receive update from observable.
        """
        raise NotImplementedError(f"ObserverInterface: update not implemented for E: {str(E)} and M: {str(M)}")
    
    
    def update_many(self, instances = dict[E, M]) -> None:
        """
        Receive updates from observable.
        """
        raise NotImplementedError(f"ObserverInterface: update_many not implemented for E: {str(E)} and M: {str(M)}")
    
    def __getitem__(self, item: E) -> M:
        value = str(item)
        return self.d[value]


    def __len__(self) -> int:
        return len(self.d)


    def __iter__(self) -> Iterator[E]:
        return iter(self.d)
