from decimal import Decimal
import os
import aiohttp
import asyncio
from typing import List

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull

    ##########################################################################################
    # Retriever Retrieves Liquid option instruments for volatility surface area subscription #
    ##########################################################################################

class ServiceRetrieveDeribitLiquidOptionInstruments():

    ## retrieved instruments list does not include the index instrumet (eg. btc_usd), this must be added at the execution service. 

    def __init__(self):
        self.base_url = 'https://deribit.com/api/v2/public'

    async def async_setup(self):
        await TaskInstrumentsPull().run(currency='BTC')
        self.store_instrument = StoreInstruments()
        
    async def main(self):
        await self.async_setup()
        store_instruments = self.store_instrument.get_deribit_instruments()
        instruments = [x for x in list(store_instruments.values()) if x.kind == 'option']
        liquid_instrument_names = await self.fetch_all(instruments=instruments)
        result = [x for x in instruments if x.instrument_name in liquid_instrument_names]

        return result
        
    async def fetch(self, instrument:ModelInstrument) -> List:
        async with aiohttp.ClientSession() as session:
            async with session.get(url= f'{self.base_url}/get_order_book?depth=10&instrument_name={instrument.instrument_name}') as response:
                data = await response.json()
                return(data)
            
    async def fetch_all(self, instruments:List) -> List:
        batch_size = 30
        tasks = []
        for i in range(0, len(instruments), batch_size):
            batch = instruments[i:i+batch_size]
            batch_tasks = [asyncio.create_task(self.fetch(instrument)) for instrument in batch]
            tasks.extend(batch_tasks)
            await asyncio.sleep(0.25)
        l = await asyncio.gather(*tasks)
        
        ## filter all results to ensure that the derivative has $5k 24h trading volume and is not trading ATM
        results = []
        for x in l:
            result = x.get('result', {})
            stats = result.get('stats', {})
            volume_usd = Decimal(stats.get('volume_usd', 0))
            if volume_usd > Decimal('5000'):
                instrument_name = result['instrument_name']
                underlying_price = Decimal(result.get('underlying_price', 0))
                index_price = Decimal(result.get('index_price', 0))
                if index_price != Decimal('0') and abs(underlying_price - index_price) / index_price > Decimal('0.00025'):
                    results.append(instrument_name)
        return results
