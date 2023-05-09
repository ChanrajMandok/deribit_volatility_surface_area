import sys
import traceback
from singleton_decorator import singleton

from deribit_arb_app.model.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.subjects.subject_indicator_bsm_implied_volatillity import SubjectIndicatorBsmImpliedVolatility

    ##################################################################
    # Store Manages & Stores Indicator Bsm Implied Volatilty objects #
    ##################################################################

@singleton
class StoreSubjectIndicatorBsmImpliedVolatilty():

    def __init__(self) -> None:
        self.subject_indicatorBsmImpliedVolatilty = {}

    def update_subject(self, key: str, indicator_bsm_implied_volatility: ModelIndicatorBsmImpliedVolatility):
        
        if not key in self.subject_indicatorBsmImpliedVolatilty:
            self.subject_indicatorBsmImpliedVolatilty[key] = \
                SubjectIndicatorBsmImpliedVolatility(indicator_bsm_implied_volatility)
        try:
            self.subject_indicatorBsmImpliedVolatilty[key].set_instance(indicator_bsm_implied_volatility)
        except Exception as e:
            print(e)
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)
        
    def get_subject(self, key: str) -> SubjectIndicatorBsmImpliedVolatility:
        if not key in self.subject_indicatorBsmImpliedVolatilty:
            self.subject_indicatorBsmImpliedVolatilty[key] = \
                SubjectIndicatorBsmImpliedVolatility()
        return self.subject_indicatorBsmImpliedVolatilty[key]