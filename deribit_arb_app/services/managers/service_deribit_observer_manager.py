import os
import asyncio
import traceback
from typing import Optional

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument

from deribit_arb_app.model.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.store.store_subject_indicator_bsm_implied_volatilty import StoreSubjectIndicatorBsmImpliedVolatilty
from deribit_arb_app.observers.observer_indicator_annualised_return_spread import ObserverIndicatorAnnualisedReturnSpread
    
    ############################################
    # Service Handles & Manages Live Observers # 
    ############################################

class ServiceDeribitObserversManager():
    
    def __init__(self):
        self.index = ModelIndex(index_name="btc_usd")
        self.observer_indicator_annualised_return_spread = ObserverIndicatorAnnualisedReturnSpread()
        self.store_subject_indicator_bsm_implied_volatilty = StoreSubjectIndicatorBsmImpliedVolatilty()
    
    async def manager_observers(self,
                            instruments_subscribables: Optional[list[ModelInstrument]],
                            instruments_unsubscribables: Optional[list[ModelInstrument]]):

        if instruments_subscribables is not None:
            for instrument in instruments_subscribables:
                if instrument != self.index:
                    indicator = ModelIndicatorBsmImpliedVolatility(
                        instrument=instrument,
                        index=self.index
                    )
                    self.observer_indicator_annualised_return_spread.attach_indicator(indicator)

        # Check if there are any live observers before detaching the index
        # if len(self.store_subject_indicator_bsm_implied_volatilty.indicators) == 0:
        #     instruments_unsubscribables.append(self.index)
                
        # if instruments_unsubscribables is not None:
        #     for instrument in instruments_unsubscribables:
        #         if instrument != self.index:
        #             key = ModelIndicatorBsmImpliedVolatility.generate_key(instrument, self.index)
        #             indicator = self.store_subject_indicator_bsm_implied_volatilty.get(key)
        #             if indicator:
        #                 self.observer_indicator_annualised_return_spread.detach_indicator(key)

        #     self.store_subject_indicator_bsm_implied_volatilty.update()