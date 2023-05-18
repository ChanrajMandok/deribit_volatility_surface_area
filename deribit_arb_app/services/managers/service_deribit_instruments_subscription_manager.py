import os
import asyncio
import traceback

from typing import List, Tuple
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.services.retrievers.service_deribit_liquid_instruments_retriever import ServiceDeribitLiquidInstrumentsRetriever
    
    ##########################################################################
    # Service Handles & Manages instrument subscriptions and Unsubscriptions # 
    ##########################################################################

class ServiceDeribitInstrumentsSubscriptionManager():
    
    def __init__(self, queue:asyncio.Queue):
        self.queue = queue
        self.previous_instruments = None
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.instruments_refresh_increment = os.environ['INSTRUMENTS_REFRESH']
        self.liquid_instruments_retriever = ServiceDeribitLiquidInstrumentsRetriever()
    
    async def manage_instrument_subscribables(self, currency: str, kind: str) -> Tuple[List[ModelInstrument], List[ModelInstrument]]:
            while True:
                instruments = await self.liquid_instruments_retriever.main(populate=False, currency=currency, kind=kind)
                instrument_names = [instrument.instrument_name for instrument in instruments]

                if self.previous_instruments is None:
                    instruments_subscribables = instruments
                    instruments_unsubscribables = []
                else:
                    previous_instrument_names = [instrument.instrument_name for instrument in self.previous_instruments]
                    instruments_subscribables = list(filter(lambda instrument: instrument.instrument_name not in previous_instrument_names, instruments))
                    instruments_unsubscribables = list(filter(lambda instrument: instrument.instrument_name not in instrument_names, self.previous_instruments))

                self.previous_instruments = instruments
                
                print(len(instruments_subscribables),len(instruments_unsubscribables))
                await self.queue.put((instruments_subscribables, instruments_unsubscribables))
                await asyncio.sleep(360)

    def _get_instrument_names(self, instruments):
        return [instrument.instrument_name for instrument in instruments]

    async def a_coroutine_subscribe(self, subscribables: List[ModelInstrument]):
        try:
            await self.deribit_subscribe.subscribe(subscribables=subscribables, snapshot=False)
        except asyncio.exceptions.TimeoutError:
            pass
        except Exception:
            traceback.print_exc()

    async def a_coroutine_unsubscribe(self, unsubscribables: List[ModelInstrument]): 
        await self.deribit_subscribe.unsubscribe(unsubscribables=unsubscribables)