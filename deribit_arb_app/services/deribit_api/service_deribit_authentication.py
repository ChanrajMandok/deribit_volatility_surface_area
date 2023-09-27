import os
import json

from singleton_decorator import singleton

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging

    ##########################################################
    # Service retrieves Deribit Authentication via Websocket #
    ##########################################################

@singleton
class ServiceDeribitAuthentication():

    def __init__(self):

        self.deribit_messaging = ServiceDeribitMessaging()

        self.params = {
                    "grant_type": "client_credentials",
                    "client_id": f'{os.environ.get("CLIENT_ID", None)}',
                    "client_secret": f'{os.environ.get("CLIENT_SECRET", None)}'
                }

        self.method = "public/auth"

        self.msg = ModelMessage(
            msg_id=self.deribit_messaging.generate_id(self.method),
            method=self.method,
            params=self.params
        )

    def authenticate(self, websocket):

        return websocket.send(json.dumps(self.msg.build_message()))



