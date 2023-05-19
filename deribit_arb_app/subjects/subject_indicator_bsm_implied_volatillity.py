from deribit_arb_app.subjects.subject_interface import SubjectInterface
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility

    ###############################################################################################################
    # Subject wraps Indicator Bsm Implied Volatility (Subject) in  subject-observer logic & adds to observer List #
    ###############################################################################################################

class SubjectIndicatorBsmImpliedVolatility(SubjectInterface):

    def __init__(self, instance: ModelIndicatorBsmImpliedVolatility) -> None:
        super().__init__(instance)