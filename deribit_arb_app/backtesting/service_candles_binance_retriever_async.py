import os
import aiohttp
import asyncio

from binance.client import BaseClient
from datetime import datetime, timedelta

    ################################################
    # Service Retrieves Candles From Binance Async #
    ################################################

class ServiceCandlesBinanceRetrieverAsync:
    """
    A class to asynchronously retrieve candle data from Binance.
    """
    
    def __init__(self):
        """Initializes the base_url from environment variable."""
        self.base_url = os.environ['BINANCE_BASE_URL']
        
    def main(self, 
             symbol: str,
             lookback_period: int) -> list:
        """
        Main function to be called to retrieve candle data.
        """
        timestamps = self.ts_increments(lookback_period=lookback_period)
        result = asyncio.run(self.fetch_all(timestamps=timestamps, symbol=symbol))
        return result     
    
    async def fetch(self, 
                    symbol: str,
                    timestamp_end: int,
                    timestamp_start: int,
                    max_retries: int = 2) -> list:
        """
        Asynchronous function to fetch candle data between two timestamps.
        """
        
        interval = BaseClient.KLINE_INTERVAL_1MINUTE
        retries = 0
        data = []
        
        while retries < max_retries:
            async with aiohttp.ClientSession() as session:
                url = (f'{self.base_url}/api/v3/klines?symbol={symbol}&interval={interval}'
                       f'&startTime={timestamp_start}&endTime={timestamp_end}&limit=1000')
                async with session.get(url) as response:
                    data = await response.json()
                    if len(data) == 1000:
                        break
                    else:
                        retries += 1
        return data
            
    async def fetch_all(self,
                        symbol: str,
                        timestamps: list ) -> list:
        """
        Asynchronous function to fetch candle data for multiple timestamps.
        """
        
        tasks = []
        for i in range(1, len(timestamps), 1):
            task = asyncio.create_task(self.fetch(timestamp_start=timestamps[i], timestamp_end=timestamps[i-1], symbol=symbol)) 
            tasks.append(task)
        list_of_candle_list = await asyncio.gather(*tasks)
        result = [x for y in list_of_candle_list for x in y]
        return result
    
    def ts_increments(self, lookback_period: int) -> list:
        """
        Function to create timestamps increments.
        """
        
        increment = 1000    
        lookback_period = lookback_period + (increment - lookback_period % increment) if lookback_period % increment > 0 else lookback_period
        end_time = datetime.now().replace(second=0, microsecond=0)
        
        start_date = end_time - timedelta(minutes=lookback_period + increment)
        date_from_0 = int((start_date - datetime(1970, 1, 1)).total_seconds() * 1000)
        date_to = int((end_time - datetime(1970, 1, 1)).total_seconds() * 1000)
        
        t1 = []
        date_from = max(date_to - increment*60*1000, date_from_0)
        while date_to > date_from_0:
            t1.append(date_from)
            date_from -= increment*60*1000
            date_to -= increment*60*1000
            
        return t1