from abc import ABC, abstractmethod

from deribit_arb_app.model.model_observable import ModelObservable
from deribit_arb_app.observables.observable_interface import ObservableInterface

    ######################################
    # Observable Object Store Interface #
    ######################################

class StoreObservableInterface(ABC):

    @abstractmethod
    def update_observable(self, observable: ModelObservable):
        pass
        
    @abstractmethod
    def get_observable(self, observable: ModelObservable) -> ObservableInterface:
        pass