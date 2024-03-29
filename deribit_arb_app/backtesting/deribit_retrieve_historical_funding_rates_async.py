import os
import aiohttp
import asyncio

from datetime import timedelta, datetime

    #########################################################
    # Backtest Retrieves Historical Funding Rates via async #
    #########################################################

class ServiceDeribitRetrieveHistoricalFundingRatesAsync:
    """
    A service class responsible for asynchronously retrieving historical funding
    rates from Deribit. It fetches the historical data within the specified
    lookback period and returns a list of the retrieved data.
    """

    def __init__(self):
        self.base_url = os.environ['BASE_HTTP_URL']


    def main(self, 
             lookback_period: int) -> list[dict]:
        """
        The main method to be called to retrieve historical funding rates.
        """
        timestamps = self.time_increments(lookback_period=lookback_period)
        result = asyncio.run(self.fetch_all(timestamps=timestamps))
        return result


    async def fetch(self, 
                    timestamp_end: int , 
                    timestamp_start: int) -> list:
        """
        Asynchronously fetches the historical funding rates between the given timestamps.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=f'{self.base_url}/public/get_funding_rate_history',
                params={
                    'end_timestamp': timestamp_end,
                    'instrument_name': 'BTC-PERPETUAL',
                    'start_timestamp': timestamp_start
                }
            ) as response:
                data = await response.json()
                return data['result']


    async def fetch_all(self, 
                        timestamps: list) -> list:
        """
        Asynchronously fetches all historical funding rates for the given list of timestamps.
        """
        tasks = [asyncio.create_task(self.fetch(timestamp_start=timestamps[i],
                                                timestamp_end=timestamps[i - 1]))
                 for i in range(1, len(timestamps), 1)]
        list_of_candle_list = await asyncio.gather(*tasks)
        return [x for y in list_of_candle_list for x in y]


    def time_increments(self, lookback_period: int) -> list:
        """
        Generates a list of timestamps in increments based on the lookback period.
        """
        # Adjusting the lookback period
        lookback_period = lookback_period + (744 - lookback_period % 744) \
                                                   if lookback_period % 744 > 0 else lookback_period

        end_time = datetime.now().replace(second=0, microsecond=0)
        start_date = end_time - timedelta(hours=lookback_period) - timedelta(hours=744)

        date_from_0 = int((start_date - datetime(1970, 1, 1)).total_seconds() * 1000)
        date_to = int((end_time - datetime(1970, 1, 1)).total_seconds() * 1000)

        t1 = []
        date_from = max(date_to, date_from_0)

        while date_to > date_from_0:
            t1.append(date_from)
            date_from -= 2678400000 
            date_to -= 2678400000  

        return t1