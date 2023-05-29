from singleton_decorator import singleton

from deribit_arb_app.subjects.subject_indicator import SubjectIndicator
from deribit_arb_app.store.store_subjectable_interface import StoreSubjectableInterface
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility

    ##################################################################
    # Store Manages & Stores Indicator Bsm Implied Volatilty objects #
    ##################################################################

@singleton
class StoreSubjectIndicatorBsmImpliedVolatilty(StoreSubjectableInterface):

    def __init__(self) -> None:
        self.subject_indicatorBsmImpliedVolatilty = {}
        
    def update_subject(self, indicator_bsm_implied_volatility: ModelIndicatorBsmImpliedVolatility):

        if indicator_bsm_implied_volatility is None:
            return
  
        if indicator_bsm_implied_volatility.name not in self.subject_indicatorBsmImpliedVolatilty:
            self.subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.name] = \
                SubjectIndicator(indicator_bsm_implied_volatility)
            self.subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.name].set_instance(indicator_bsm_implied_volatility)
            print(f"{indicator_bsm_implied_volatility.name}: {round(indicator_bsm_implied_volatility.Implied_volatilty,4)}")
        else:
            existing_value = self.subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.name].instance.Implied_volatilty
            new_value =  indicator_bsm_implied_volatility.Implied_volatilty
            if existing_value == new_value:
                return  # don't update if the existing value is the same as the prior value
            else:
                self.subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.name].set_instance(indicator_bsm_implied_volatility)
                print(f"{indicator_bsm_implied_volatility.name}: {round(indicator_bsm_implied_volatility.Implied_volatilty,4)}")

    def get_subject(self, key: str) :
        if not key in self.subject_indicatorBsmImpliedVolatilty:
            self.subject_indicatorBsmImpliedVolatilty[key] = \
                SubjectIndicator.subject_indicator_bsm_implied_volatillity()
        return self.subject_indicatorBsmImpliedVolatilty[key]

    def remove_subject(self, key: str):
        if key is None:
            return

        if key in self.subject_indicatorBsmImpliedVolatilty:
            del self.subject_indicatorBsmImpliedVolatilty[key]