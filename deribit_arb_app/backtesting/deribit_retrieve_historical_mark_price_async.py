import os
import aiohttp
import asyncio

from datetime import timedelta, datetime

    ############################################################
    # Backtest Retrieves Historical Mark Price Rates via async #
    ############################################################

class ServiceDeribitRetrieveHistoricaMarkPriceAsync:
    """
    Service class designed to asynchronously retrieve historical mark prices 
    from Deribit's public API. The class fetches historical data within a specified 
    lookback period and returns it as a list of dictionaries.
    """

    def __init__(self):
        self.base_url = os.environ['BASE_HTTP_URL']


    def main(self, 
             lookback_period: int) -> list[dict]:
        """
        Entry point for fetching historical mark prices. Calls other class methods
        to generate timestamps, perform asynchronous fetching, and flatten the results.
        """
        timestamps = self.time_increments(lookback_period=lookback_period)
        result = asyncio.run(self.fetch_all(timestamps=timestamps))
        return result


    async def fetch(self, 
                    timestamp_end: int,
                    timestamp_start: int) -> list:
        """
        Asynchronous method to fetch historical mark prices between the given timestamps.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=f'{self.base_url}/public/get_funding_rate_history',
                    params={'end_timestamp': timestamp_end, 'instrument_name': 'BTC-PERPETUAL',
                            'start_timestamp': timestamp_start}) as response:
                data = await response.json()
                return data['result']


    async def fetch_all(self,
                        timestamps: list) -> list:
        """
        Constructs tasks for asynchronous fetching of all historical mark prices based on the
        given timestamps.
        """
        tasks = [asyncio.create_task(self.fetch(timestamp_start=timestamps[i],
                                                timestamp_end=timestamps[i - 1]))
                 for i in range(1, len(timestamps))]
        list_of_candle_list = await asyncio.gather(*tasks)
        return [item for sublist in list_of_candle_list for item in sublist]


    def time_increments(self, lookback_period: int) -> list:
        """
        Generate a list of timestamps in increments based on the lookback period.
        """
        # Adjusting the lookback period
        lookback_period = lookback_period + (744 - lookback_period % 744) \
                                                   if lookback_period % 744 > 0 else lookback_period
        
        # Setting start and end times
        end_time = datetime.now().replace(second=0, microsecond=0)
        start_date = end_time - timedelta(hours=lookback_period) - timedelta(hours=744)
        
        # Calculating timestamp in milliseconds from epoch time
        date_from_0 = int((start_date - datetime(1970, 1, 1)).total_seconds() * 1000)
        date_to = int((end_time - datetime(1970, 1, 1)).total_seconds() * 1000)
        
        t1 = []
        date_from = max(date_to, date_from_0)
        # Creating a list of timestamps in increments
        while date_to > date_from_0:
            t1.append(date_from)
            date_from -= 2678400000  # 31 days in milliseconds
            date_to -= 2678400000  # Adjusting the range

        return t1
