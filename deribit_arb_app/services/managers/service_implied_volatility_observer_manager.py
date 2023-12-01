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
    """
    Manages the observers for implied volatility. This service handles the attaching and detaching
    of observers to model instruments for tracking their implied volatility.
    """

    def __init__(self, implied_volatility_queue: asyncio.Queue):
        self.implied_volatility_queue = implied_volatility_queue
        # Initialize the observer for BSM implied volatility
        self.observer_indicator_bsm_implied_volatility = \
                            ObserverIndicatorBsmImpliedVolatility(self.implied_volatility_queue)
        
    async def manager_observers(self,
                                index: ModelSubscribableIndex,
                                volatility_index: ModelSubscribableVolatilityIndex,
                                subscribables: Optional[list[ModelSubscribableInstrument]],
                                unsubscribables: Optional[list[ModelSubscribableInstrument]]):
        """
        Manages the attachment and detachment of observers to and from instruments.
        """
        # Attach observers to new instruments
        if subscribables  and len(subscribables) > 0:
            for instrument in subscribables:
                # Check if the object is a subscribable instrument
                if isinstance(instrument, ModelSubscribableInstrument):
                    object_name = f"BSM Implied Volatility-{instrument.name}"
                    # Determine option type based on the instrument's name
                    option_type = EnumOptionType.CALL if object_name.rstrip()[-1] == 'C' \
                                                                            else EnumOptionType.PUT
                    try:
                        # Create an indicator for the instrument and attach an observer
                        indicator = ModelIndicatorBsmImpliedVolatility(
                                                                       index=index,
                                                                       name=object_name,
                                                                       instrument=instrument,
                                                                       option_type=option_type,
                                                                       volatility_index=volatility_index
                                                                       )
                        self.observer_indicator_bsm_implied_volatility.attach_indicator(indicator)
                    except Exception as e:
                        logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                                f"Stack trace: {traceback.format_exc()}")
                
            logger.info(f"{self.__class__.__name__}: {len(subscribables)} Observers attached ")
                    
        # Detach observers from unsubscribed instruments
        if unsubscribables and len(unsubscribables) > 0:
            logger.info(f"{self.__class__.__name__}: {len(unsubscribables)} Observers dettached")
            for instrument in unsubscribables:
                try:
                    # Detach the index and volatility index if there are no active observers
                    if len(self.observer_indicator_bsm_implied_volatility) == 0:
                        unsubscribables.extend([index, volatility_index])
                    # Check if the object is a subscribable instrument
                    if isinstance(instrument, ModelSubscribableInstrument):
                        # Generate the key for the instrument and detach the observer
                        key = ModelIndicatorBsmImpliedVolatility.generate_key_from_instrument(instrument)
                        self.observer_indicator_bsm_implied_volatility.detach_indicator(key)
                except Exception as e:
                    logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                            f"Stack trace: {traceback.format_exc()}")
                