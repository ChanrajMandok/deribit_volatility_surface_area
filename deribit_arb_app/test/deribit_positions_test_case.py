import sys
import traceback
import asynctest
import asyncio

from deribit_arb_app.store.store_deribit_positions import StoreDeribitPositions
from deribit_arb_app.services.deribit_positions import DeribitPositions
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentPull


class DeribitPositionsTestCase(asynctest.TestCase):

    def setUp(self):
        TaskInstrumentPull().run()
        self.deribit_positions = DeribitPositions(currency="BTC")
        self.store_deribit_positions = StoreDeribitPositions()
        self.my_loop = asyncio.new_event_loop()

    async def positions_coroutine(self):
        await asyncio.wait_for(self.deribit_positions.get(), timeout=100.0) 

    def test_positions_get(self):
        try:
            self.my_loop.run_until_complete(self.positions_coroutine())
        except Exception as e:
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)
        finally:
            self.my_loop.close()
            self.assertTrue(len(self.store_deribit_positions.get_deribit_positions(currency="BTC")) > 0)

    def tearDown(self):
       self.my_loop.close()