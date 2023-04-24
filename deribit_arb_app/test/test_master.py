import asyncio
import unittest

from deribit_arb_app.store.store_deribit_authorization import StoreDeribitAuthorization
from deribit_arb_app.services.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.services.service_deribit_authentication import ServiceDeribitAuthentication
from deribit_arb_app.services.service_deribit_websocket_connector import ServiceDeribitWebsocketConnector
from deribit_arb_app.store.store_deribit_account_summary import StoreDeribitAccountSummary
from deribit_arb_app.services.service_deribit_account_summary import ServiceDeribitAccountSummary

class TestMasterTestCase(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        cls.store_deribit_authorization = StoreDeribitAuthorization()
        cls.deribit_authentication = ServiceDeribitAuthentication()
        cls.deribit_messaging = ServiceDeribitMessaging()
        cls.connector = ServiceDeribitWebsocketConnector()
        cls.deribit_account_summary = ServiceDeribitAccountSummary(currency="BTC")
        cls.store_deribit_account_summary = StoreDeribitAccountSummary()

    async def authenticate(self):
        async with self.connector.get_websocket() as websocket:
            await self.deribit_authentication.authenticate(websocket)

            while websocket.open:
                response = await websocket.recv()
                self.deribit_messaging.message_handle(response)
                if self.store_deribit_authorization.is_authorized():
                    break

    async def test_authenticate(self):
        await self.authenticate()
        self.assertTrue(self.store_deribit_authorization.is_authorized())

    async def test_account_summary_get(self):
        if not self.store_deribit_authorization.is_authorized():
            await self.authenticate()

        await asyncio.wait_for(self.deribit_account_summary.get(), timeout=100.0)
        self.assertIsNotNone(self.store_deribit_account_summary.get_deribit_account_summary())