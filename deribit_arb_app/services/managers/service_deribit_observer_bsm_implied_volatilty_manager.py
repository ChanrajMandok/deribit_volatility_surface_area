from typing import Optional

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency

from deribit_arb_app.observers.observer_indicator_bsm_implied_volatility import ObserverIndicatorBsmImpliedVolatility
from deribit_arb_app.store.store_subject_indicator_bsm_implied_volatilty import StoreSubjectIndicatorBsmImpliedVolatilty
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility    

    #####################################################
    # Service Handles, Builds  & Manages Live Observers # 
    #####################################################

class ServiceDeribitObserverBsmImpliedVolatilityManager():
    
    def __init__(self):
        self.observer_indicator_bsm_implied_volatility = ObserverIndicatorBsmImpliedVolatility()
        self.store_subject_indicator_bsm_implied_volatilty = StoreSubjectIndicatorBsmImpliedVolatilty()
        
    async def manager_observers(self,
                                index :ModelIndex,
                                subscribables: Optional[list[ModelInstrument]],
                                unsubscribables: Optional[list[ModelInstrument]]):

    # observers are internally generated & managed so no corountine is required
        if subscribables is not None:
            for instrument in subscribables:
                if instrument != index:
                    indicator = ModelIndicatorBsmImpliedVolatility(
                        instrument=instrument,
                        index=index
                    )
                    self.observer_indicator_bsm_implied_volatility.attach_indicator(indicator)
                    print(f"{str(indicator.key)} observer attached")

        # only detach index from unsubscribables if their are no live observers
        if len(self.store_subject_indicator_bsm_implied_volatilty.indicators) == 0:
            unsubscribables.append(self.index)
                
        if unsubscribables is not None:
            for instrument in unsubscribables:
                if instrument != index:
                    key = ModelIndicatorBsmImpliedVolatility.generate_key(instrument)
                    indicator = self.store_subject_indicator_bsm_implied_volatilty.get_subject(key)
                    if indicator:
                        self.observer_indicator_bsm_implied_volatility.detach_indicator(key)
                        print(f"{str(indicator.key)} observer detached")
                        ## remove if the indicator exists, else do nothing
                        
        