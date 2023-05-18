import os
import asyncio
import traceback
from typing import Optional

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.model.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.store.store_subject_indicator_bsm_implied_volatilty import StoreSubjectIndicatorBsmImpliedVolatilty
from deribit_arb_app.observers.observer_indicator_annualised_return_spread import ObserverIndicatorAnnualisedReturnSpread
    
    #####################################################
    # Service Handles, Builds  & Manages Live Observers # 
    #####################################################

class ServiceDeribitObserversManager():
    
    def __init__(self):
        self.index = ModelIndex(index_name="btc_usd")
        self.observer_indicator_annualised_return_spread = ObserverIndicatorAnnualisedReturnSpread()
        self.store_subject_indicator_bsm_implied_volatilty = StoreSubjectIndicatorBsmImpliedVolatilty()
        
    async def manager_observers(self,
                            subscribables: Optional[list[ModelInstrument]],
                            unsubscribables: Optional[list[ModelInstrument]]):

    # observers are internally generated & managed so not corountine is required
        if subscribables is not None:
            for instrument in subscribables:
                if instrument != self.index:
                    indicator = ModelIndicatorBsmImpliedVolatility(
                        instrument=instrument,
                        index=self.index
                    )
                    self.observer_indicator_annualised_return_spread.attach_indicator(indicator)
                    print(f"{}")

        # only detach index from unsubscribables if their are no live observers
        if len(self.store_subject_indicator_bsm_implied_volatilty.indicators) == 0:
            unsubscribables.append(self.index)
                
        if unsubscribables is not None:
            for instrument in unsubscribables:
                if instrument != self.index:
                    key = ModelIndicatorBsmImpliedVolatility.generate_key(instrument)
                    indicator = self.store_subject_indicator_bsm_implied_volatilty.get_subject(key)
                    if indicator:
                        self.observer_indicator_annualised_return_spread.detach_indicator(key)
                        ## remove if the indicator exists, else do nothing
                        
        