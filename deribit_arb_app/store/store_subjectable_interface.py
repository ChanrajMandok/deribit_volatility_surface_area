from abc import ABC, abstractmethod

from deribit_arb_app.subjects.subject_interface import SubjectInterface
from deribit_arb_app.subjects.subject_index_price import SubjectIndexPrice
from deribit_arb_app.model.model_subjectable import ModelSubjectable


class StoreSubjectableInterface(ABC):

    @abstractmethod
    def update_subject(self, subjectable: ModelSubjectable):
        pass
        
    @abstractmethod
    def get_subject(self, subjectable: ModelSubjectable) -> SubjectInterface:
        pass