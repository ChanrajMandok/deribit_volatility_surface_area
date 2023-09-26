import asyncio
import traceback

from typing import Optional
from singleton_decorator import singleton

from deribit_arb_app.services import logger
from deribit_arb_app.enums.enum_option_type import EnumOptionType
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.model.model_subscribable_volatility_index import \
                                       ModelSubscribableVolatilityIndex
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.observers.observer_indicator_bsm_implied_volatility import \
                                            ObserverIndicatorBsmImpliedVolatility
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import \
                                                         ModelIndicatorBsmImpliedVolatility

    #####################################################
    # Service Handles, Builds  & Manages Live Observers # 
    #####################################################

@singleton
class ServiceImpliedVolatilityObserverManager:
    def __init__(self, implied_volatility_queue: asyncio.Queue):
        self.implied_volatility_queue = implied_volatility_queue
        self.observer_indicator_bsm_implied_volatility = \
            ObserverIndicatorBsmImpliedVolatility(self.implied_volatility_queue)
        
    async def manager_observers(self,
                                index :ModelSubscribableIndex,
                                volatility_index:ModelSubscribableVolatilityIndex,
                                subscribables: Optional[list[ModelSubscribableInstrument]],
                                unsubscribables: Optional[list[ModelSubscribableInstrument]]):

    # observers are internally generated & managed so no corountine is required
        if subscribables is not None:
            for instrument in subscribables:
                if type(instrument) == ModelSubscribableInstrument:
                    object_name = f"BSM Implied Volatility-{instrument.name}"
                    option_type = EnumOptionType.CALL if object_name.rstrip()[-1] == 'C' else EnumOptionType.PUT
                    try:
                        indicator = ModelIndicatorBsmImpliedVolatility(
                            index=index,
                            name=object_name,
                            instrument=instrument,
                            option_type=option_type,
                            volatility_index=volatility_index
                        )
                        self.observer_indicator_bsm_implied_volatility.attach_indicator(indicator)
                        # print(f"{str(indicator.key)} observer attached")
                    except Exception as e:
                        logger.error(f"{self.__class__.__name__}: Error: {str(e)}. Stack trace: {traceback.format_exc()}")
                    
        if unsubscribables is not None:
            for instrument in unsubscribables:
                try:
                    # only detach index from unsubscribables if their are no live observers
                    if len(self.observer_indicator_bsm_implied_volatility) == 0:
                        unsubscribables.extend([index, volatility_index])
                    if type(instrument) == ModelSubscribableInstrument:
                        key = ModelIndicatorBsmImpliedVolatility.generate_key(instrument)
                        self.observer_indicator_bsm_implied_volatility.detach_indicator(key)
                        # print(f"{str(indicator.key)} observer detached")
                except Exception as e:
                        logger.error(f"{self.__class__.__name__}: Error: {str(e)}. Stack trace: {traceback.format_exc()}")