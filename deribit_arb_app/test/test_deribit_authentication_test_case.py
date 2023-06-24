import unittest

from deribit_arb_app.store.store_deribit_authorization import StoreDeribitAuthorization
from deribit_arb_app.services.deribit_api.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_authentication import ServiceDeribitAuthentication
from deribit_arb_app.services.deribit_api.service_deribit_websocket_connector import ServiceDeribitWebsocketConnector

    #######################################################################
    # TestCase Testing Authentication Object in StoreDeribitAuthorization #
    #######################################################################

class TestDeribitAuthenticationTestCase(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        super().setUp()
        self.deribit_authentication = ServiceDeribitAuthentication()
        self.deribit_messaging = ServiceDeribitMessaging()
        self.store_deribit_authorization = StoreDeribitAuthorization()

    async def a_coroutine(self):
        self.deribit_authentication.get_authorization()

        async with ServiceDeribitWebsocketConnector() as websocket:

            await self.deribit_authentication.authenticate(websocket)

            while websocket.open:
                response = await websocket.recv()
                self.deribit_messaging.message_handle(response)
                break

    async def test_authenticate(self):
        # If Auth object already exists in store then check that it is has Auth Token 
        auth = self.store_deribit_authorization.get_authorization()
        # Else create Auth object and check that it is has Auth Token
        if not auth:
            try:
                await self.a_coroutine()
                self.assertTrue(self.store_deribit_authorization.is_authorized())
            except Exception as e:
                self.fail(f"Test failed due to exception: {str(e)}")
        else:
            self.assertTrue(self.store_deribit_authorization.is_authorized())