from typing import Dict
import json
from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.services.deribit_authentication import DeribitAuthentication
from deribit_arb_app.services.deribit_messaging import DeribitMessaging
from deribit_arb_app.services.deribit_websocket_connector import DeribitWebsocketConnector
from deribit_arb_app.model.model_position import ModelPosition


@Singleton
class DeribitPositions:

    def __init__(self, currency: str):

        self.deribit_messaging = DeribitMessaging()

        self.params = {
                    "currency": currency,
                    "kind": "future"
                }

        self.method = "private/get_positions"

        self.msg_id = self.deribit_messaging.generate_id(self.method)

        self.msg = ModelMessage(
            msg_id=self.msg_id,
            method=self.method,
            params=self.params
        )

    async def get(self) -> Dict[str, Dict[str, ModelPosition]]:

        async with DeribitWebsocketConnector().get_websocket() as websocket:

            await DeribitAuthentication().authenticate(websocket)
            await websocket.send(json.dumps(self.msg.build_message()))

            while websocket.open:
                response = await websocket.recv()
                self.deribit_messaging.message_handle(response)
                
                # handle the message and get the id
                id, positions = self.deribit_messaging.message_handle(response)

                # if the id matches the initial msg id, we can break the loop
                if id == self.msg_id:
                    return positions


