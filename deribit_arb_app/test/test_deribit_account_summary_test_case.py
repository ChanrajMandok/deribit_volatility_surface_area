import asyncio
import asynctest

from deribit_arb_app.store.store_deribit_account_summary import StoreDeribitAccountSummary
from deribit_arb_app.services.service_deribit_account_summary import ServiceDeribitAccountSummary

    #########################################################################
    # TestCase Testing Account Summary is within StoreDeribitAccountSummary #
    #########################################################################

class TestDeribitAccountSummaryTestCase(asynctest.TestCase):

    def setUp(self):
        super().setUp()
        self.store_deribit_account_summary = StoreDeribitAccountSummary()
        self.deribit_account_summary = ServiceDeribitAccountSummary(currency="BTC")
        
    async def a_coroutine(self):        
        await asyncio.wait_for(self.deribit_account_summary.get(), timeout=10.0)

    def test_account_summary_get(self):
        self.loop.run_until_complete(self.a_coroutine())
        self.assertIsNotNone(self.store_deribit_account_summary.get_deribit_account_summary())