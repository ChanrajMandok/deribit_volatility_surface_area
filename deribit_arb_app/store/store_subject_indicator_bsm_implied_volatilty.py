import math

from singleton_decorator import singleton

from deribit_arb_app.store.store_subjectable_interface import StoreSubjectableInterface
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.subjects.subject_indicator_bsm_implied_volatillity import SubjectIndicatorBsmImpliedVolatility

    ##################################################################
    # Store Manages & Stores Indicator Bsm Implied Volatilty objects #
    ##################################################################

@singleton
class StoreSubjectIndicatorBsmImpliedVolatilty(StoreSubjectableInterface):

    def __init__(self) -> None:
        self.subject_indicatorBsmImpliedVolatilty = {}
        
    def update_subject(self, key: str, indicator_bsm_implied_volatility: ModelIndicatorBsmImpliedVolatility):

        if indicator_bsm_implied_volatility is None:
            return
  
        if key not in self.subject_indicatorBsmImpliedVolatilty:
            self.subject_indicatorBsmImpliedVolatilty[key] = \
                SubjectIndicatorBsmImpliedVolatility(indicator_bsm_implied_volatility)
            self.subject_indicatorBsmImpliedVolatilty[key].set_instance(indicator_bsm_implied_volatility)
            print(f"{key}: {round(indicator_bsm_implied_volatility.value,4)}")
        else:
            existing_value = self.subject_indicatorBsmImpliedVolatilty[key].instance.value
            new_value =  indicator_bsm_implied_volatility.value
            if existing_value == new_value:
                return  # don't update if the existing value is the same as the prior value
            else:
                self.subject_indicatorBsmImpliedVolatilty[key].set_instance(indicator_bsm_implied_volatility)
                print(f"{key}: {round(indicator_bsm_implied_volatility.value,4)}")

    def get_subject(self, key: str) -> SubjectIndicatorBsmImpliedVolatility:
        if not key in self.subject_indicatorBsmImpliedVolatilty:
            self.subject_indicatorBsmImpliedVolatilty[key] = \
                SubjectIndicatorBsmImpliedVolatility()
        return self.subject_indicatorBsmImpliedVolatilty[key]
    
    def remove_subject(self, key: str):
        if key is None:
            return

        if key in self.subject_indicatorBsmImpliedVolatilty:
            del self.subject_indicatorBsmImpliedVolatilty[key]