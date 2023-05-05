import sys
import asyncio
import traceback
import asynctest
from typing import List

from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.services.retrievers.service_retrieve_deribit_liquid_option_instruments import ServiceRetrieveDeribitLiquidOptionInstruments

    ###########################################################################
    # Plot Subscribe, Observe and plot Asset Specific Volatility Surface Area #
    ###########################################################################

class PlotDeribitVolatiltySurfaceArea():
    
    def __init__(self):
        self.liquid_instruments_list_retriever = ServiceRetrieveDeribitLiquidOptionInstruments()
        self.deribit_subscribe = ServiceDeribitSubscribe()
        
    async def a_coroutine_subscribe(self, instruments:List):
        try:
            await asyncio.wait_for(self.deribit_subscribe.subscribe(
                    subscribables=instruments, snapshot=False), timeout=300)
        except asyncio.exceptions.TimeoutError:
            pass
        except Exception as e:
             _, _, exc_traceback = sys.exc_info()
             traceback.print_tb(exc_traceback, limit=None, file=None)
             
    def main(self):
        loop = asyncio.new_event_loop()
        instruments = loop.run_until_complete(self.liquid_instruments_list_retriever.main())
        loop.run_until_complete(self.a_coroutine_subscribe(instruments))