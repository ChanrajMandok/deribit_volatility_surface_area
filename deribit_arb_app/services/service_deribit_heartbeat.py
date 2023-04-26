import json
from singleton_decorator import singleton
from deribit_arb_app.model.model_message import ModelMessage

from deribit_arb_app.converters.converter_json_to_heartbeat import ConverterJsonToHeartbeat

from deribit_arb_app.services.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.services.service_deribit_websocket_connector import ServiceDeribitWebsocketConnector

    #####################################################
    # Service retrieves Deribit Heartbeat via Websocket #
    #####################################################

@singleton
class ServiceDeribitHeartbeat:

    def __init__(self):

        self.deribit_messaging = ServiceDeribitMessaging()

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

        async with ServiceDeribitWebsocketConnector() as websocket:

            await websocket.send(json.dumps(self.msg.build_message()))

            while websocket.open:

                response = await websocket.recv()

                result = ConverterJsonToHeartbeat(response).convert()

                if result == "test_request":
                    await websocket.send(json.dumps(self.msg_test.build_message()))



