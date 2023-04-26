from deribit_arb_app.subjects.subject_interface import SubjectInterface
from deribit_arb_app.model.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread

class SubjectIndicatorAnnualisedReturnSpread(SubjectInterface):

    # wraps the AnnualisedReturnSpread subject with the subject-observer logic to attach-detach observers to the observers list

    def __init__(self, instance: ModelIndicatorAnnualisedReturnSpread) -> None:
        super().__init__(instance)

