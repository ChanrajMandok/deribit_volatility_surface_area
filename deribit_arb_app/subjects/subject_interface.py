from abc import ABC
from typing import Generic, List, TypeVar
from deribit_arb_app.model.model_subjectable import ModelSubjectable
from deribit_arb_app.observers.observer_interface import ObserverInterface

T=TypeVar('T', ModelSubjectable, ModelSubjectable)

    ###############################################################################################
    # Subject interface declaring set of methods which manage subscriptions and observer subjects #
    ###############################################################################################

class SubjectInterface(ABC, Generic[T]):

    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    def __init__(self, instance: T) -> None:
        super().__init__()
        self.instance = instance
        self.observers = []

    def get_instance(self) -> T:
        return self.instance

    def set_instance(self, instance: T) -> None:
        self.instance = instance
        self.notify()

    def attach(self, observer: ObserverInterface) -> None:
        self.observers.append(observer)

    def detach(self, observer: ObserverInterface) -> None:
        self.observers.remove(observer)

    def notify(self) -> None:
        for observer in self.observers:
            observer.update()
