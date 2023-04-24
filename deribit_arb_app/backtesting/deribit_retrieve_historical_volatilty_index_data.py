import os
import json
import asyncio
import websockets

from datetime import datetime, timedelta

    ################################################################
    # Backtest Retrieves Historical Volatility Index via Websocket #
    ################################################################

class DeribitRetrieveHistoricalVolatilityIndexData():
 
    def __init__(self):
        self.base_ws_url = os.environ['BASE_WS_URL']
        self.msg = {
            "jsonrpc": "2.0",
            "id": 833,
            "method": "public/get_volatility_index_data",
            "params": {
                "currency": "BTC",
                "start_timestamp": 1599373800000,
                "end_timestamp": 1599376800000,
                "resolution": "60"
            }
        }

async def call_api(self, msg):
    async with websockets.connect(f"{self.base_ws_url}") as websocket:
        await websocket.send(msg)
        while websocket.open:
            response = await websocket.recv()
            # do something with the response...
            print(response)

def get_timestamps(start_date, end_date, interval):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    current = start

    while current < end:
        next_date = current + timedelta(days=interval)
        yield int(current.timestamp() * 1000), int(next_date.timestamp() * 1000)
        current = next_date

start_date = "2020-09-01"
end_date = "2020-10-01"
interval_in_days = 1

for start_timestamp, end_timestamp in get_timestamps(start_date, end_date, interval_in_days):
    msg["params"]["start_timestamp"] = start_timestamp
    msg["params"]["end_timestamp"] = end_timestamp
    print(f"Fetching data for period {datetime.fromtimestamp(start_timestamp / 1000)} - {datetime.fromtimestamp(end_timestamp / 1000)}")
    asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))