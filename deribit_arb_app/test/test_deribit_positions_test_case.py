import sys
import asyncio
import traceback
import asynctest

from deribit_arb_app.store.store_deribit_positions import StoreDeribitPositions
from deribit_arb_app.services.service_deribit_positions import ServiceDeribitPositions

    ########################################################################
    # TestCase Testing StoreDeribitPositions().get() to see open Positions #
    ########################################################################

class TestDeribitPositionsTestCase(asynctest.TestCase):

    async def setUp(self):
        super().setUp()
        self.deribit_positions = ServiceDeribitPositions(currency="BTC")
        self.store_deribit_positions = StoreDeribitPositions()
        self.my_loop = asyncio.new_event_loop()

    async def positions_coroutine(self):
        await asyncio.wait_for(self.deribit_positions.get(), timeout=10) 

    def test_positions_get(self):
        try:
            self.my_loop.run_until_complete(self.positions_coroutine())
        except Exception as e:
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)
        finally:
            self.my_loop.close()
            self.assertTrue(len(self.store_deribit_positions.get_deribit_positions(currency="BTC")) > 0)