
import sys
import json
import traceback

from typing import List, Dict

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.model.model_subscribable import ModelSubscribable
from deribit_arb_app.services.deribit_api.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_websocket_connector import ServiceDeribitWebsocketConnector

    ########################################################
    # Service Provides interface to Subscribe to Websocket #
    ########################################################

class ServiceDeribitSubscribe(ModelSubscribable):

    def __init__(self):

        self.deribit_messaging = ServiceDeribitMessaging()
        self.subscriptions = []

    async def send_instructions(self, method: str, params: Dict, snapshot: bool = False):

        msg_id = self.deribit_messaging.generate_id(method)

        msg = ModelMessage(
            msg_id=msg_id,
            method=method,
            params=params
        )

        async with ServiceDeribitWebsocketConnector() as websocket:
            await websocket.send(json.dumps(msg.build_message()))
            while websocket.open:
                try:
                    response = await websocket.recv()
                    id_or_method, _ = self.deribit_messaging.message_handle(response)
                    if snapshot and id_or_method == "subscription":
                        break
                except Exception as e:
                    print(e)
                    _, _, exc_traceback = sys.exc_info()
                    traceback.print_tb(exc_traceback, limit=None, file=None)

    async def subscribe(self, subscribables: List[ModelSubscribable], snapshot: bool):

        method = "public/subscribe"

        params = {
            "channels": []
        }

        for subscribable in subscribables:
            params["channels"].append(subscribable.channel_name)
            # print(f"SUBSCRIBED {subscribable.channel_name}")
            if snapshot==False:
                self.subscriptions.append(subscribable)
        
        try:
            await self.send_instructions(method, params, snapshot)
        except Exception as e:
            print(e)
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)

    async def unsubscribe(self, unsubscribables: List[ModelSubscribable]):

        method = "public/unsubscribe"

        params = {
            "channels": []
        }

        for unsubscribable in unsubscribables:
            if unsubscribable in self.subscriptions:
                self.subscriptions.remove(unsubscribable)
            params["channels"].append(unsubscribable.channel_name)
            # print(f"UNSUBSCRIBED {unsubscribable.channel_name}")
            
        await self.send_instructions(method, params)