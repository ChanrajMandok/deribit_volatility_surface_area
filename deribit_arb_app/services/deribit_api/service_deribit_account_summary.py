import json

from singleton_decorator import singleton

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_authentication import \
                                                     ServiceDeribitAuthentication
from deribit_arb_app.services.deribit_api.service_deribit_websocket_connector import \
                                                      ServiceDeribitWebsocketConnector

    ###########################################################
    # Service retrieves Deribit Account Summary via Websocket #
    ###########################################################

@singleton
class ServiceDeribitAccountSummary:
    """
    Service class to get the account summary from Deribit.
    """

    def __init__(self, currency: str):
        self.deribit_messaging = ServiceDeribitMessaging()

        self.params = {
            "currency": currency,
            "extended": True
        }

        self.method = "private/get_account_summary"

        self.msg_id = self.deribit_messaging.generate_id(self.method)

        self.msg = ModelMessage(msg_id=self.msg_id,
                               method=self.method,
                               params=self.params
                               )
        
        
    async def get(self):
        """
        Retrieve the account summary from Deribit through websocket.        
        """
        async with ServiceDeribitWebsocketConnector() as websocket:
            await ServiceDeribitAuthentication().authenticate(websocket)
            await websocket.send(json.dumps(self.msg.build_message()))
            
            while websocket.open:
                response = await websocket.recv()

                # handle the message and get the id
                id, account_summary = self.deribit_messaging.message_handle(response)

                # if the id matches the initial msg id, we can break the loop
                if id == self.msg_id:
                    return account_summary
