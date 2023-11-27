import json

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_websocket_connector import \
                                                      ServiceDeribitWebsocketConnector
                                                      
    #######################################################
    # Service retrieves Deribit instruments via Websocket #
    #######################################################

class ServiceDeribitInstruments:
    """
    Service class to fetch instruments for a specified currency and kind from Deribit.

    This class communicates with the Deribit API to retrieve a list of
    instruments, based on the specified currency and kind (e.g., 'option', 'future').
    """

    def __init__(self, currency: str, kind: str):
        self.deribit_messaging = ServiceDeribitMessaging()

        self.params = {
            "currency": currency,
            "kind": kind,
            "expired": False
        }

        self.method = "public/get_instruments"

        self.msg_id = self.deribit_messaging.generate_id(self.method)

        self.msg = ModelMessage(msg_id=self.msg_id,
                                method=self.method,
                                params=self.params
                                )


    async def get(self) -> dict[str, ModelSubscribableInstrument]:
        """
        Fetch the instruments for the specified currency and kind using a websocket connection.
        """
        async with ServiceDeribitWebsocketConnector() as websocket:
            await websocket.send(json.dumps(self.msg.build_message()))

            while websocket.open:
                response = await websocket.recv()

                # Handle the message and extract the id and instruments data
                id, instruments = self.deribit_messaging.message_handle(response)

                # If the id matches the initial msg id, return the instruments data
                if id == self.msg_id:
                    return instruments