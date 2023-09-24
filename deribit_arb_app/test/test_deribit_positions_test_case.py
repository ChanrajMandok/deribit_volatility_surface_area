import sys
import asyncio
import unittest
import traceback

from deribit_arb_app.services.deribit_api.service_deribit_positions import \
                                                     ServiceDeribitPositions
from deribit_arb_app.store.store_deribit_positions import StoreDeribitPositions

    ########################################################################
    # TestCase Testing StoreDeribitPositions().get() to see open Positions #
    ########################################################################

class TestDeribitPositionsTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        super().setUp()
        self.deribit_positions = ServiceDeribitPositions(currency="BTC")
        self.store_deribit_positions = StoreDeribitPositions()

    async def positions_coroutine(self):
        await asyncio.wait_for(self.deribit_positions.get(), timeout=10) 

    async def test_positions_get(self):
        try:
            await self.positions_coroutine()
            self.assertTrue(len(self.store_deribit_positions.get_deribit_positions(currency="BTC")) > 0)
        except Exception as e:
            self.fail(f"Test failed due to exception: {str(e)}")