from deribit_arb_app.model.model_order_book import ModelOrderBook
from deribit_arb_app.subjects.subject_interface import SubjectInterface

    #########################################################################################
    # Subject wraps Order Book (Subject) in  subject-observer logic & adds to observer List #
    #########################################################################################

class SubjectOrderBook(SubjectInterface):

    def __init__(self, instance: ModelOrderBook) -> None:
        super().__init__(instance)
        