import sys
import traceback
from singleton_decorator import singleton

from deribit_arb_app.store.store_subjectable_interface import StoreSubjectableInterface
from deribit_arb_app.model.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.subjects.subject_indicator_bsm_implied_volatillity import SubjectIndicatorBsmImpliedVolatility

    ##################################################################
    # Store Manages & Stores Indicator Bsm Implied Volatilty objects #
    ##################################################################

class StoreSubjectIndicatorBsmImpliedVolatilty(StoreSubjectableInterface):

    def __init__(self) -> None:
        self.__subject_indicatorBsmImpliedVolatilty = {}

    def update_subject(self, indicator_bsm_implied_volatility: ModelIndicatorBsmImpliedVolatility):
        
        if indicator_bsm_implied_volatility is None:
            return

        if not indicator_bsm_implied_volatility.key in self.__subject_indicatorBsmImpliedVolatilty:
            self.__subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.key] = \
                SubjectIndicatorBsmImpliedVolatility(indicator_bsm_implied_volatility)
        try:
            self.__subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.key].set_instance(indicator_bsm_implied_volatility)
        except Exception as e:
            print(e)
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)

    def get_subject(self, indicator_bsm_implied_volatility: ModelIndicatorBsmImpliedVolatility) -> SubjectIndicatorBsmImpliedVolatility:
        if not indicator_bsm_implied_volatility.key in self.__subject_indicatorBsmImpliedVolatilty:
            self.__subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.key] = \
                SubjectIndicatorBsmImpliedVolatility(indicator_bsm_implied_volatility)
        return self.__subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.key]