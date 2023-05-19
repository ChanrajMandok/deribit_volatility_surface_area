import os
import asyncio
import aiohttp
from typing import List, Optional
from decimal import Decimal

from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull
from deribit_arb_app.services.handlers.service_deribit_static_orderbook_handler import ServiceDeribitStaticOrderbookHandler

    ################################################################################
    # Manager Manages Liquid instruments to Maturity Matching Put-Call Instruments #
    ################################################################################

class ServiceDeribitPutCallParityOptionsManager():

    ## similar to observer manager assume that liquid instruments retriever is managing subset of available instruments, this service takes the 
    # subscribables & unsubscribables and finds all mathcing put_call instruments  
    
    def __init__(self):
        pass 

    async def manager_subscriptables(self,
                                     subscribables: Optional[list[ModelInstrument]],
                                     unsubscribables: Optional[list[ModelInstrument]]):
    
        
        for instrument in subscribables:
            name = instrument.instrument_name
            type = instrument.

            ## use custom sorting algorith, look on stack overflow to ensure optimised searh and sorting