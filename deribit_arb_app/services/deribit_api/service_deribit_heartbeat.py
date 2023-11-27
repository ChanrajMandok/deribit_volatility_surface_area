import json

from singleton_decorator import singleton

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.converters.converter_json_to_heartbeat import \
                                            ConverterJsonToHeartbeat
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_websocket_connector import \
                                                      ServiceDeribitWebsocketConnector

    #####################################################
    # Service retrieves Deribit Heartbeat via Websocket #
    #####################################################

@singleton
class ServiceDeribitHeartbeat:
    """
    Service class for managing heartbeat with the Deribit API.
    
    This class is designed to handle the heartbeat mechanism, ensuring 
    that the connection to Deribit remains active and responsive.
    """

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
            msg_id=self.deribit_messaging.generate_id(self.method_test),
            method=self.method_test,
            params=self.params_test
        )


    async def set(self):
        """
        Set the heartbeat for the websocket connection to Deribit and 
        handle any test requests sent by Deribit as part of the heartbeat mechanism.
        """
        async with ServiceDeribitWebsocketConnector() as websocket:
            await websocket.send(json.dumps(self.msg.build_message()))

            while websocket.open:
                response = await websocket.recv()

                result = ConverterJsonToHeartbeat(response).convert()

                if result == "test_request":
                    await websocket.send(json.dumps(self.msg_test.build_message()))