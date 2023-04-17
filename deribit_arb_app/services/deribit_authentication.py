import os
import json

from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.services.deribit_messaging import DeribitMessaging


@Singleton
class DeribitAuthentication:

    def __init__(self):

        self.deribit_messaging = DeribitMessaging()

        self.params = {
                    "grant_type": "client_credentials",
                    "client_id": f'{os.environ["CLIENT_ID"]}',
                    "client_secret": f'{os.environ["CLIENT_SECRET"]}'
                }

        self.method = "public/auth"

        self.msg = ModelMessage(
            msg_id=self.deribit_messaging.generate_id(self.method),
            method=self.method,
            params=self.params
        )

    def authenticate(self, websocket):

        return websocket.send(json.dumps(self.msg.build_message()))



