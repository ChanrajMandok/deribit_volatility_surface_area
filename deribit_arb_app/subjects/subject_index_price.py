from deribit_arb_app.model.model_index_price import ModelIndexPrice
from deribit_arb_app.subjects.subject_interface import SubjectInterface

    ##########################################################################################
    # Subject wraps Index Price (Subject) in  subject-observer logic & adds to observer List #
    ##########################################################################################

class SubjectIndexPrice(SubjectInterface):

    def __init__(self, instance: ModelIndexPrice) -> None:
        super().__init__(instance)
        