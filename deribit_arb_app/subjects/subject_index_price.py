from deribit_arb_app.model.model_index_price import ModelIndexPrice
from deribit_arb_app.subjects.subject_interface import SubjectInterface


class SubjectIndexPrice(SubjectInterface):

    # wraps the IndexPrice subject with the subject-observer logic to attach-detach observers to the observers list

    def __init__(self, instance: ModelIndexPrice) -> None:
        super().__init__(instance)
        