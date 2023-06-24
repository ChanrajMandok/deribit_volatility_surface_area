import asyncio
import unittest

from deribit_arb_app.store.store_deribit_account_summary import StoreDeribitAccountSummary
from deribit_arb_app.services.deribit_api.service_deribit_account_summary import ServiceDeribitAccountSummary

    #########################################################################
    # TestCase Testing Account Summary is within StoreDeribitAccountSummary #
    #########################################################################

class TestDeribitAccountSummaryTestCase(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        super().setUp()
        self.store_deribit_account_summary = StoreDeribitAccountSummary()
        self.deribit_account_summary = ServiceDeribitAccountSummary(currency="BTC")

    async def a_coroutine(self):
        await asyncio.wait_for(self.deribit_account_summary.get(), timeout=10.0)

    async def test_account_summary_get(self):
        await self.a_coroutine()
        self.assertIsNotNone(self.store_deribit_account_summary.get_deribit_account_summary())
