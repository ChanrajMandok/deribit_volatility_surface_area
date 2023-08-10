import json

from typing import Dict
from singleton_decorator import singleton

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.model.model_position import ModelPosition

from deribit_arb_app.services.deribit_api.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_authentication import ServiceDeribitAuthentication
from deribit_arb_app.services.deribit_api.service_deribit_websocket_connector import ServiceDeribitWebsocketConnector

    ################################################################################
    # Service Retrieves Deribit Orderbook Summary by Currency & Kind via Websocket #
    ################################################################################

@singleton
class ServiceDeribitGetOrderbookSummary():

    def __init__(self, currency: str, kind: str):

        self.deribit_messaging = ServiceDeribitMessaging()

        self.params = {
                    "currency": currency,
                    "kind": kind
                }

        self.method = "public/get_book_summary_by_currency"

        self.msg_id = self.deribit_messaging.generate_id(self.method)

        self.msg = ModelMessage(
            msg_id=self.msg_id,
            method=self.method,
            params=self.params
        )

    async def get(self) -> Dict[str, Dict[str, ModelPosition]]:

        async with ServiceDeribitWebsocketConnector() as websocket:

            await ServiceDeribitAuthentication().authenticate(websocket)
            await websocket.send(json.dumps(self.msg.build_message()))

            while websocket.open:
                response = await websocket.recv()
                
                # handle the message and get the id
                id, data = self.deribit_messaging.message_handle(response)

                # if the id matches the initial msg id, we can break the loop
                if id == self.msg_id:
                    return data