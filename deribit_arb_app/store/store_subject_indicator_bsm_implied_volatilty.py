import asyncio

from singleton_decorator import singleton
from collections.abc import AsyncGenerator

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
        self.update_queue = asyncio.Queue()
        
    async def update_subject(self, indicator_bsm_implied_volatility: ModelIndicatorBsmImpliedVolatility):

        if indicator_bsm_implied_volatility is None:
            return
  
        if indicator_bsm_implied_volatility.name not in self.subject_indicatorBsmImpliedVolatilty:
            self.subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.name] = \
                SubjectIndicator(indicator_bsm_implied_volatility)
            self.subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.name].set_instance(indicator_bsm_implied_volatility)
            print(f"{indicator_bsm_implied_volatility.name}: {round(indicator_bsm_implied_volatility.Implied_volatilty,4)}")
            try:
                await self.update_queue.put(self.subject_indicatorBsmImpliedVolatilty)
            except Exception as e:
                print(f"Exception in store queue: {e}")
        else:
            existing_value = self.subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.name].instance.Implied_volatilty
            new_value =  indicator_bsm_implied_volatility.Implied_volatilty
            if existing_value == new_value:
                return  # don't update if the existing value is the same as the prior value
            else:
                self.subject_indicatorBsmImpliedVolatilty[indicator_bsm_implied_volatility.name].set_instance(indicator_bsm_implied_volatility)
                print(f"{indicator_bsm_implied_volatility.name}: {round(indicator_bsm_implied_volatility.Implied_volatilty,4)}")
                await self.update_queue.put(self.subject_indicatorBsmImpliedVolatilty)
                
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
            
    async def stream_subjects_view(self) -> AsyncGenerator[dict[str, ModelIndicatorBsmImpliedVolatility], None]:
        """
        Async generator function that emits dictionary items in a stream.
        """
        while True:
            if len(self.subject_indicatorBsmImpliedVolatilty.keys()) > 0:
                updated_subjects = await self.update_queue.get()
                yield updated_subjects
                self.update_queue.task_done()
                
                
        ## anywhere we update subject must now be awaited
