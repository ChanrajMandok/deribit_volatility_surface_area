import json

from singleton_decorator import singleton

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.model.model_subscribable_instrument import \
                                      ModelSubscribableInstrument
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.model.model_orderbook_summary import ModelOrderbookSummary
from deribit_arb_app.services.deribit_api.service_deribit_authentication import \
                                                     ServiceDeribitAuthentication
from deribit_arb_app.services.deribit_api.service_deribit_websocket_connector import \
                                                      ServiceDeribitWebsocketConnector
    ################################################################################
    # Service Retrieves Deribit Orderbook Summary by Currency & Kind via Websocket #
    ################################################################################

@singleton
class ServiceDeribitOrderbookStoreUpdaterByInstrument:
    """
    Service class to fetch the orderbook summary for a specified instrument from Deribit.
    """
    
    def __init__(self, 
                 instrument: str):
        self.deribit_messaging = ServiceDeribitMessaging()

        self.params = {
            "instrument_name" : instrument
        }

        self.method = "public/get_book_summary_by_instrument"

        self.msg_id = self.deribit_messaging.generate_id(self.method)

        self.msg = ModelMessage(msg_id=self.msg_id,
                                method=self.method,
                                params=self.params
                                )


    async def get(self) -> dict[str, dict[str, ModelOrderbookSummary]]:
        """
        Fetch the orderbook summary for the specified instrument via a websocket connection.
        """
        async with ServiceDeribitWebsocketConnector() as websocket:
            await ServiceDeribitAuthentication().authenticate(websocket)
            await websocket.send(json.dumps(self.msg.build_message()))

            while websocket.open:
                response = await websocket.recv()
                
                # Handle the message and retrieve the id and data
                id, data = self.deribit_messaging.message_handle(response)

                # If the id matches the initial msg id, exit the loop
                if id == self.msg_id:
                    return data