import json

from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.services.deribit_authentication import DeribitAuthentication
from deribit_arb_app.services.deribit_messaging import DeribitMessaging
from deribit_arb_app.services.deribit_websocket_connector import DeribitWebsocketConnector


@Singleton
class DeribitAccountSummary:

    def __init__(self, currency: str):

        self.deribit_messaging = DeribitMessaging()

        self.params = {
                    "currency": currency,
                    "extended": True
                }

        self.method = "private/get_account_summary"

        self.msg_id = self.deribit_messaging.generate_id(self.method)

        self.msg = ModelMessage(
            msg_id=self.msg_id,
            method=self.method,
            params=self.params
        )

    async def get(self):

        async with DeribitWebsocketConnector().get_websocket() as websocket:

            await DeribitAuthentication().authenticate(websocket)
            await websocket.send(json.dumps(self.msg.build_message()))
            
            while websocket.open:
                response = await websocket.recv()

                # handle the message and get the id
                id, account_summary = self.deribit_messaging.message_handle(response)

                # if the id matches the initial msg id, we can break the loop
                if id == self.msg_id:
                    return account_summary


