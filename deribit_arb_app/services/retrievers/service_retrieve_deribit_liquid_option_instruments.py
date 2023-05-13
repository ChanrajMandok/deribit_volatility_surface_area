import os
import asyncio
import aiohttp
from typing import List
from decimal import Decimal

from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull
from deribit_arb_app.services.handlers.service_deribit_static_orderbook_handler import ServiceDeribitStaticOrderbookHandler

    #################################################
    # Retriever Retrieves Liquid option instruments #
    #################################################

class ServiceRetrieveDeribitLiquidOptionInstruments():

    ## retrieved instruments list does not include the index instrumet (eg. btc_usd), this must be added at the execution service. 

    def __init__(self):        
        self.base_url = os.environ['BASE_HTTP_URL']
        self.service_deribit_static_orderbook_handler = ServiceDeribitStaticOrderbookHandler()
        self.minimum_liquidity_threshold = os.environ['MINIMUM_LIQUIDITY_THRESHOLD']
    
    async def async_setup(self, currency:str, kind:str):
        await TaskInstrumentsPull().run(currency, kind)
        self.store_instrument = StoreInstruments()
        
    async def main(self, populate:bool, currency:str, kind:str) -> List[str]:
        await self.async_setup(currency=currency, kind=kind)
        store_instruments = self.store_instrument.get_deribit_instruments()
        instruments = [x for x in list(store_instruments.values()) if x.kind == kind]
        liquid_instrument_names = await self.fetch_all(instruments=instruments, populate=populate)
        result = [x.instrument_name for x in instruments if x.instrument_name in liquid_instrument_names]
        return result
        
    async def fetch(self, instrument:ModelInstrument) -> List:
        async with aiohttp.ClientSession() as session:
            async with session.get(url= f'{self.base_url}/public/get_order_book?depth=10&instrument_name={instrument.instrument_name}') as response:
                data = await response.json()
                return(data)
            
    async def fetch_all(self, instruments:List, populate:bool) -> List:
        batch_size = 20
        tasks = []
        sem = asyncio.Semaphore(20)  # Adjust this number to limit concurrent tasks

        async def bound_fetch(sem, instrument):
            async with sem:  # This will block if too many tasks are running
                return await self.fetch(instrument)

        for i in range(0, len(instruments), batch_size):
            batch = instruments[i:i+batch_size]
            batch_tasks = [asyncio.create_task(bound_fetch(sem, instrument)) for instrument in batch]
            tasks.extend(batch_tasks)
            await asyncio.sleep(1)

        l = await asyncio.gather(*tasks)
        
        results = []
        instrument_names = []
        for x in l:
            keys = ['instrument_name','best_bid_price','best_ask_price','best_bid_amount','best_ask_amount']
            result = x.get('result', {})
            stats = result.get('stats', {})
            volume_usd = Decimal(stats.get('volume_usd', 0))
            ## check that instrument has atleast 5k of trading vol in last 24h
            if volume_usd > Decimal(self.minimum_liquidity_threshold):
                instrument_name = result['instrument_name']
                underlying_price = Decimal(result.get('underlying_price', 0))
                index_price = Decimal(result.get('index_price', 0))
                ##check that instrument has bid or ask that is not 0
                (best_bid_size, best_bid_price) = (Decimal(result.get('best_bid_amount', 0)), Decimal(result.get('best_bid_price', 0)))
                (best_ask_size, best_ask_price) = (Decimal(result.get('best_ask_amount', 0)), Decimal(result.get('best_ask_price', 0)))
                if (best_bid_size != 0 and best_bid_price != 0) or (best_ask_size != 0 and best_ask_price != 0):
                ##check that instrument is not trading as spot underlying_price != index price  
                    if index_price != Decimal('0') and abs(underlying_price - index_price) / index_price > Decimal('0.00025'):
                        instrument_names.append(instrument_name)
                        if populate:
                            results.append({key: result.get(key, 0) for key in keys})

        if populate:
            ## if populate use static orderbook screenshots to populate orderbook stores, providing base before subscription
            [self.service_deribit_static_orderbook_handler.set_orderbooks(result=value) for value in results]
        return instrument_names
