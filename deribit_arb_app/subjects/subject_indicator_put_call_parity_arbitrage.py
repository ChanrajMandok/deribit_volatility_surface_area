from deribit_arb_app.subjects.subject_interface import SubjectInterface
from deribit_arb_app.model.indicator_models.model_indicator_put_call_parity_arbitrage import ModelIndicatorPutCallParityArbitrage

    ########################################################################################################
    # Subject wraps Put Call Parity Arbitrage (Subject) in  subject-observer logic & adds to observer List #
    ########################################################################################################

class SubjectIndicatorPutCallParityArbitrage(SubjectInterface):

    def __init__(self, instance: ModelIndicatorPutCallParityArbitrage) -> None:
        super().__init__(instance)

