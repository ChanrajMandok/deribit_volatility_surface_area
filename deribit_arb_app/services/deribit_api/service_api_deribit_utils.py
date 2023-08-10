import asyncio
import traceback

from typing import List
from deribit_arb_app.model.model_subscribable_instrument import ModelSubscribableInstrument
from deribit_arb_app.services.deribit_api.service_deribit_subscribe import ServiceDeribitSubscribe

    ##########################################################################################
    # Service Implements Deribit API Corountines to Subscribe to Deribit Streams & Snapshots #
    ##########################################################################################

class ServiceApiDeribitUtils:

    def __init__(self) -> None:
        self.deribit_subscribe = ServiceDeribitSubscribe()
    
    async def a_coroutine_subscribe(self, subscribables: List[ModelSubscribableInstrument], snapshot: bool = False):
        try:
            await self.deribit_subscribe.subscribe(subscribables=subscribables, snapshot=snapshot)
        except asyncio.exceptions.TimeoutError:
            pass
        except Exception:
            traceback.print_exc()

    async def a_coroutine_unsubscribe(self, unsubscribables: List[ModelSubscribableInstrument]): 
        await self.deribit_subscribe.unsubscribe(unsubscribables=unsubscribables)