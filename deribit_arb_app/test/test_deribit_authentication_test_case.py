import asyncio
import asynctest

from deribit_arb_app.store.store_deribit_authorization import StoreDeribitAuthorization

from deribit_arb_app.services.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.services.service_deribit_authentication import ServiceDeribitAuthentication
from deribit_arb_app.services.service_deribit_websocket_connector import ServiceDeribitWebsocketConnector


class TestDeribitAuthenticationTestCase(asynctest.TestCase):

    def setUp(self):
        self.deribit_authentication = ServiceDeribitAuthentication()
        self.deribit_messaging = ServiceDeribitMessaging()
        self.store_deribit_authorization = StoreDeribitAuthorization()

        self.my_loop = asyncio.new_event_loop()

    async def a_coroutine(self):
        async with ServiceDeribitWebsocketConnector().get_websocket() as websocket:

            await self.deribit_authentication.authenticate(websocket)

            while websocket.open:
                response = await websocket.recv()
                self.deribit_messaging.message_handle(response)
                break

    def test_authenticate(self):
        try:
            self.my_loop.run_until_complete(self.a_coroutine())
        finally:
            self.my_loop.close()
        self.assertTrue(self.store_deribit_authorization.is_authorized())

    def tearDown(self):
       self.my_loop.close()
