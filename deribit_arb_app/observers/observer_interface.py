from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T=TypeVar('T')

class ObserverInterface(ABC, Generic[T]):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self) -> None:
        """
        Receive update from subject.
        """
        pass

    @abstractmethod
    def get(self) -> T:
        pass
