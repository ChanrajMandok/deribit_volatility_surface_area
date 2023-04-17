import json

from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.converters.json_to_heartbeat import JsonToHeartbeat
from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.services.deribit_messaging import DeribitMessaging
from deribit_arb_app.services.deribit_websocket_connector import DeribitWebsocketConnector


@Singleton
class DeribitHeartbeat:

    def __init__(self):

        self.deribit_messaging = DeribitMessaging()

        self.params = {
                    "interval": 30
                }

        self.method = "public/set_heartbeat"

        self.msg = ModelMessage(
            msg_id=self.deribit_messaging.generate_id(self.method),
            method=self.method,
            params=self.params
        )

        self.params_test = {}

        self.method_test = "public/test"

        self.msg_test = ModelMessage(
            msg_id=self.deribit_messaging.generate_id(self.method),
            method=self.method,
            params=self.params
        )

    async def set(self):

        async with DeribitWebsocketConnector().get_websocket() as websocket:

            await websocket.send(json.dumps(self.msg.build_message()))

            while websocket.open:

                response = await websocket.recv()

                result = JsonToHeartbeat(response).convert()

                if result == "test_request":
                    await websocket.send(json.dumps(self.msg_test.build_message()))



