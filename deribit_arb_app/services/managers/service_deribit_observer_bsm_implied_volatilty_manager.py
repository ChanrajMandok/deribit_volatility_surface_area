import asyncio

from typing import Optional
from singleton_decorator import singleton

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.observers.observer_indicator_bsm_implied_volatility import ObserverIndicatorBsmImpliedVolatility
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility    

    #####################################################
    # Service Handles, Builds  & Manages Live Observers # 
    #####################################################

@singleton
class ServiceDeribitObserverBsmImpliedVolatilityManager:
    def __init__(self, implied_volatility_queue: asyncio.Queue):
        self.implied_volatility_queue = implied_volatility_queue
        self.observer_indicator_bsm_implied_volatility = ObserverIndicatorBsmImpliedVolatility(self.implied_volatility_queue)
        
    async def manager_observers(self,
                                index :ModelIndex,
                                subscribables: Optional[list[ModelInstrument]],
                                unsubscribables: Optional[list[ModelInstrument]]):

    # observers are internally generated & managed so no corountine is required
        if subscribables is not None:
            for instrument in subscribables:
                if instrument != index:
                    object_name = f"BSM Implied Volatility-{instrument.instrument_name}"
                    indicator = ModelIndicatorBsmImpliedVolatility(
                        name=object_name,
                        instrument=instrument,
                        index=index
                    )
                    self.observer_indicator_bsm_implied_volatility.attach_indicator(indicator)
                    # print(f"{str(indicator.key)} observer attached")

        if unsubscribables is not None:
            for instrument in unsubscribables:
                # only detach index from unsubscribables if their are no live observers
                if len(self.observer_indicator_bsm_implied_volatility) == 0:
                    unsubscribables.append(index)
                if instrument != index:
                    key = ModelIndicatorBsmImpliedVolatility.generate_key(instrument)
                    self.observer_indicator_bsm_implied_volatility.detach_indicator(key)
                        # print(f"{str(indicator.key)} observer detached")
                        
        
                        
        