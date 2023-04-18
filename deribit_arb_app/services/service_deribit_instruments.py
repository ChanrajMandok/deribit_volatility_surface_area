import json
from typing import Dict, List

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.model.model_instrument import ModelInstrument

from deribit_arb_app.services.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.services.service_deribit_websocket_connector import ServiceDeribitWebsocketConnector

    #######################################################
    # Service retrieves Deribit instruments via Websocket #
    #######################################################

class ServiceDeribitInstruments:

    def __init__(self, currency: str, kind: str):

        self.deribit_messaging = ServiceDeribitMessaging()

        self.params = {
            "currency": currency,
            "kind": kind,
            "expired": False
        }

        self.method = "public/get_instruments"

        self.msg_id = self.deribit_messaging.generate_id(self.method)

        self.msg = ModelMessage(
            msg_id=self.msg_id,
            method=self.method,
            params=self.params
        )

    async def get(self) -> Dict[str, ModelInstrument]:

        async with ServiceDeribitWebsocketConnector().get_websocket() as websocket:
            
            await websocket.send(json.dumps(self.msg.build_message()))

            while websocket.open:
                response = await websocket.recv()

                # handle the message and get the id
                id, instruments = self.deribit_messaging.message_handle(response)

                # if the id matches the initial msg id, we can break the loop
                if id == self.msg_id:
                    return instruments
