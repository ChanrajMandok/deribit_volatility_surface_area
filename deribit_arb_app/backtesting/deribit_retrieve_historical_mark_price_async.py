import os
import aiohttp
import asyncio

from typing import List

from datetime import timedelta, datetime

    ############################################################
    # Backtest Retrieves Historical Mark Price Rates via async #
    ############################################################

class ServiceDeribitRetrieveHistoricaMarkPriceAsync():

    def __init__(self):
        self.base_url = os.environ['BASE_HTTP_URL']
        
    def main(self, lookback_period) -> List[dict]:
        timestamps = self.time_increments(lookback_period=lookback_period)
        result = asyncio.run(self.fetch_all(timestamps=timestamps))
        return result   
        
    async def fetch(self, timestamp_start:int, timestamp_end:int) -> List:
        async with aiohttp.ClientSession() as session:
            async with session.get(url= f'{self.base_url}/public/get_funding_rate_history?end_timestamp={timestamp_end}&instrument_name=BTC-PERPETUAL&start_timestamp={timestamp_start}') as response:
                data = await response.json()
                return(data['result'])
            
    async def fetch_all(self, timestamps:List) -> List:
        tasks = []
        for i in range(1,len(timestamps),1):
            task = asyncio.create_task(self.fetch(timestamp_start=timestamps[i], timestamp_end=timestamps[i-1])) 
            tasks.append(task)
        list_of_candle_list = await asyncio.gather(*tasks)
        result = [x for y in list_of_candle_list for x in y]
        return result
    
    def time_increments(self, lookback_period=int) -> List:    
        lookback_period=lookback_period + (744 - lookback_period % 744) if lookback_period % 744 > 0 else lookback_period
        end_time = datetime.now().replace(second=0, microsecond=0)
        
        start_date = end_time - timedelta(hours=lookback_period) - timedelta(hours=744) 
        date_from_0 = int((start_date - datetime(1970, 1, 1)).total_seconds() * 1000)
        date_to = int((end_time - datetime(1970, 1, 1)).total_seconds() * 1000)
        
        t1 = []
        date_from = max(date_to , date_from_0)
        while date_to > date_from_0:
            t1.append(date_from)
            date_from -= 2678400000
            date_to -= 2678400000
            
        return t1
    
    
        