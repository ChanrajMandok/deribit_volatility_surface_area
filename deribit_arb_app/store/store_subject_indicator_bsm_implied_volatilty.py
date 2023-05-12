import math
import asyncio
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

        ## if new indicator is None, do nothing -> we do not want to update
        if indicator_bsm_implied_volatility is None:
            return
        ## if indicator.value is nan (bsm has not been able to give a implied Vol figure) but key does not exist we can set instance
        if math.isnan(indicator_bsm_implied_volatility.value):
            if key not in self.subject_indicatorBsmImpliedVolatilty:
                self.subject_indicatorBsmImpliedVolatilty[key] = \
                    SubjectIndicatorBsmImpliedVolatility(indicator_bsm_implied_volatility)
                self.subject_indicatorBsmImpliedVolatilty[key].set_instance(indicator_bsm_implied_volatility)
                print(f"{key}: {round(indicator_bsm_implied_volatility.value,4)}")
            else:
                existing_value = self.subject_indicatorBsmImpliedVolatilty[key]
                if existing_value is not None and math.isnan(existing_value.instance.value):
                    return  # don't update if the existing value is also NaN
                else:
                    self.subject_indicatorBsmImpliedVolatilty[key].set_instance(indicator_bsm_implied_volatility)
                    print(f"{key}: {round(indicator_bsm_implied_volatility.value,4)}")
        else:
            if key not in self.subject_indicatorBsmImpliedVolatilty:
                self.subject_indicatorBsmImpliedVolatilty[key] = \
                    SubjectIndicatorBsmImpliedVolatility(indicator_bsm_implied_volatility)
                self.subject_indicatorBsmImpliedVolatilty[key].set_instance(indicator_bsm_implied_volatility)
                print(f"{key}: {round(indicator_bsm_implied_volatility.value,4)}")
            else:
                existing_value = self.subject_indicatorBsmImpliedVolatilty[key]
                if existing_value is not None and hasattr(existing_value.instance, 'value') and math.isnan(existing_value.instance.value):
                    self.subject_indicatorBsmImpliedVolatilty[key].set_instance(indicator_bsm_implied_volatility)
                    print(f"{key}: {round(indicator_bsm_implied_volatility,4)}")
                elif existing_value is None or (hasattr(existing_value.instance, 'value') and existing_value.instance.value != indicator_bsm_implied_volatility.value):
                    self.subject_indicatorBsmImpliedVolatilty[key].set_instance(indicator_bsm_implied_volatility)
                    print(f"{key}: {round(indicator_bsm_implied_volatility.value,4)}")

    def get_subject(self, key: str) -> SubjectIndicatorBsmImpliedVolatility:
        if not key in self.subject_indicatorBsmImpliedVolatilty:
            self.subject_indicatorBsmImpliedVolatilty[key] = \
                SubjectIndicatorBsmImpliedVolatility()
        return self.subject_indicatorBsmImpliedVolatilty[key]
    
    async def stream_store(self):
            """Asynchronously yield the current state of the store."""
            while True:
                await asyncio.sleep(0)  # yield control to the event loop
                yield self.subject_indicatorBsmImpliedVolatilty