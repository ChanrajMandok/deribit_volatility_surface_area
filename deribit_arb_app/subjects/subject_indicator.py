from deribit_arb_app.model.model_order_book import ModelOrderBook
from deribit_arb_app.model.model_index_price import ModelIndexPrice
from deribit_arb_app.subjects.subject_interface import SubjectInterface
from deribit_arb_app.model.indicator_models.model_indicator_volatilty_surface_area import ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.model.indicator_models.model_indicator_volatilty_surface_area import ModelIndicatorVolatilitySurfaceArea
from deribit_arb_app.model.indicator_models.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread
from deribit_arb_app.model.indicator_models.model_indicator_put_call_parity_arbitrage import ModelIndicatorPutCallParityArbitrage

    ##########################################################################################
    # Subjects wraps Indicators (Subject) in  subject-observer logic & adds to observer List #
    ##########################################################################################

class SubjectIndicator(SubjectInterface):
    
    def __init__(self, instance) -> None:
        super().__init__(instance)