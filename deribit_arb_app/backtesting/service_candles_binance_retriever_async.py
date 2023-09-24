import os
import aiohttp
import asyncio

from binance.client import BaseClient
from datetime import datetime, timedelta

    ################################################
    # Service Retrieves Candles From Binance Async #
    ################################################

class ServiceCandlesBinanceRetrieverAsync():
    
    def __init__(self):
        self.base_url = os.environ['BINANCE_BASE_URL']
        
    def main(self, lookback_period, symbol:str):
        timestamps = self.ts_increments(lookback_period=lookback_period)
        result = asyncio.run(self.fetch_all(timestamps=timestamps, symbol=symbol))
        return result     
    
    async def fetch(self, timestamp_start:int,timestamp_end:int, symbol:str, max_retries=2) -> list:
        interval = BaseClient.KLINE_INTERVAL_1MINUTE
        retries = 0
        data = []
        while retries < max_retries:
            async with aiohttp.ClientSession() as session:
                async with session.get(url= f'{self.base_url}/api/v3/klines?symbol={symbol}&interval={interval}&startTime={timestamp_start}&endTime={timestamp_end}&limit=1000') as response:
                    data = await response.json()
                    if len(data) == 1000:
                        break
                    else:
                        retries += 1
        return data
            
    async def fetch_all(self, timestamps:list, symbol:str) -> list:
        tasks = []
        for i in range(1,len(timestamps),1):
            task = asyncio.create_task(self.fetch(timestamp_start=timestamps[i], timestamp_end=timestamps[i-1], symbol=symbol)) 
            tasks.append(task)
        list_of_candle_list = await asyncio.gather(*tasks)
        result = [x for y in list_of_candle_list for x in y]
        return result
    
    def ts_increments(self, lookback_period=int) -> list:
        increment = 1000    
        lookback_period=lookback_period + (increment - lookback_period % increment) if lookback_period % increment > 0 else lookback_period
        end_time = datetime.now().replace(second=0, microsecond=0)
        
        start_date = end_time - timedelta(minutes=lookback_period+increment)
        date_from_0 = int((start_date - datetime(1970, 1, 1)).total_seconds() * 1000)
        date_to = int((end_time - datetime(1970, 1, 1)).total_seconds() * 1000)
        
        t1 = []
        date_from = max(date_to -increment*60*1000, date_from_0)
        while date_to > date_from_0:
            t1.append(date_from)
            date_from -= increment*60*1000
            date_to -= increment*60*1000
            
        return t1