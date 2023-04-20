import os
import json
import requests

from datetime import timedelta, datetime

    #########################################################
    # Backtest Retrieves Historical Funding Rates via https #
    #########################################################

class ServiceDeribitRetrieveHistoricalFundingRatesHttp():

    def __init__(self):
        self.base_url = os.environ['BASE_HTTP_URL']

    def call_api(self, lookback_period=10000):
            lookback_period=lookback_period + (744 - lookback_period % 744) if lookback_period % 744 > 0 else lookback_period
            end_time = datetime.now()
            start_date = end_time - timedelta(hours=lookback_period)

            date_from_0 = int((start_date - datetime(1970, 1, 1)).total_seconds() * 1000)
            date_to = int((end_time - datetime(1970, 1, 1)).total_seconds() * 1000)

            response_list = []
            date_from = max(date_to - 2678400000, date_from_0)
            while date_to > date_from_0:
                response = requests.get(url= f'{self.base_url}/public/get_funding_rate_history?end_timestamp={date_to}&instrument_name=BTC-PERPETUAL&start_timestamp={date_from}')
                if response.status_code != 200:
                    raise Exception(f'Request failed with status code {response.status_code}')
                data = json.loads(response.content)['result']
                response_list.extend(data)
                date_from -= 2678400000
                date_to -= 2678400000

            if len(response_list) != lookback_period-1:
                 raise Exception(f'{__class__.__name__} error with pulling historical funding rates') 

            return response_list