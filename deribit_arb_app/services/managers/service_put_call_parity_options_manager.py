import os
import asyncio
import aiohttp

from decimal import Decimal
from typing import Optional
from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull
from deribit_arb_app.model.model_subscribable_instrument import ModelSubscribableInstrument
from deribit_arb_app.services.handlers.service_deribit_static_orderbook_handler import ServiceDeribitStaticOrderbookHandler

    ################################################################################
    # Manager Manages Liquid instruments to Maturity Matching Put-Call Instruments #
    ################################################################################

@singleton
class ServicePutCallParityOptionsManager():

    ## similar to observer manager assume that liquid instruments retriever is managing subset of available instruments, this service takes the 
    # subscribables & unsubscribables and finds all mathcing put_call instruments  
    
    def __init__(self):
        pass 

    async def manager_subscriptables(self,
                                     subscribables: Optional[list[ModelSubscribableInstrument]],
                                     unsubscribables: Optional[list[ModelSubscribableInstrument]]):
    
        
        for instrument in subscribables:
            name = instrument.name
            pass

            ## use custom sorting algorith, look on stack overflow to ensure optimised searh and sorting