from deribit_arb_app.subjects.subject_interface import SubjectInterface
from deribit_arb_app.model.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread

    #######################################################################################################
    # Subject wraps Annualised Return Spread (Subject) in  subject-observer logic & adds to observer List #
    #######################################################################################################

class SubjectIndicatorAnnualisedReturnSpread(SubjectInterface):

    def __init__(self, instance: ModelIndicatorAnnualisedReturnSpread) -> None:
        super().__init__(instance)

