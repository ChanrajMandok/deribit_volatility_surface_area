from deribit_arb_app.model.model_order_book import ModelOrderBook
from deribit_arb_app.subjects.subject_interface import SubjectInterface


class SubjectOrderBook(SubjectInterface):

    # wraps the OrderBook subject with the subject-observer logic to attach-detach observers to the observers list

    def __init__(self, instance: ModelOrderBook) -> None:
        super().__init__(instance)
        