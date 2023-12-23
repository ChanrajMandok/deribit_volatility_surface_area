import asyncio
import traceback

from deribit_arb_app.services import logger
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.services.deribit_api.service_deribit_subscribe import \
                                                     ServiceDeribitSubscribe

    ##############################################################################
    # Service Implements Deribit API to Subscribe to Deribit Streams & Snapshots #
    ##############################################################################

class ServiceApiDeribitUtils:
    """Utility class for managing subscriptions with Deribit."""

    def __init__(self) -> None:
        self.deribit_subscribe = ServiceDeribitSubscribe()


    async def a_coroutine_subscribe(self, 
                                    subscribables: list[ModelSubscribableInstrument], 
                                    snapshot: bool = False):
        """
        Subscribes to given instruments on Deribit.
        """
        try:
            await self.deribit_subscribe.subscribe(subscribables=subscribables, 
                                                   snapshot=snapshot)
        except asyncio.exceptions.TimeoutError:
            pass
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                         f"Stack trace: {traceback.format_exc()}")


    async def a_coroutine_unsubscribe(self, 
                                      unsubscribables: list[ModelSubscribableInstrument]):
        """
        Unsubscribes from given instruments on Deribit.
        """
        try:
            await self.deribit_subscribe.unsubscribe(unsubscribables=unsubscribables)
        except asyncio.exceptions.TimeoutError:
            pass
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                         f"Stack trace: {traceback.format_exc()}")