import asyncio
import asynctest


from deribit_arb_app.store.store_deribit_account_summary import StoreDeribitAccountSummary

from deribit_arb_app.services.service_deribit_account_summary import ServiceDeribitAccountSummary


class TestDeribitAccountSummaryTestCase(asynctest.TestCase):

    def setUp(self):
        self.deribit_account_summary = ServiceDeribitAccountSummary(currency="BTC")
        self.store_deribit_account_summary = StoreDeribitAccountSummary()
        self.my_loop = asyncio.new_event_loop()

    async def a_coroutine(self):        
        await asyncio.wait_for(self.deribit_account_summary.get(), timeout=100.0)

    def test_account_summary_get(self):
        try:
            self.my_loop.run_until_complete(self.a_coroutine())
        finally:
            self.my_loop.close()
            self.assertIsNotNone(self.store_deribit_account_summary.get_deribit_account_summary())

    def tearDown(self):
       self.my_loop.close()
