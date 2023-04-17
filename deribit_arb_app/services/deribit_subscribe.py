import sys
import traceback
from typing import List
import json
from typing import List, Dict
from abc import ABC

from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.services.deribit_messaging import DeribitMessaging
from deribit_arb_app.services.deribit_websocket_connector import DeribitWebsocketConnector
from deribit_arb_app.model.model_exchange_subscribable import ModelExchangeSubscribable


class DeribitSubscribe(ModelExchangeSubscribable):

    def __init__(self):

        self.deribit_messaging = DeribitMessaging()
        self.subscriptions = []

    async def send_instructions(self, method: str, params: Dict, snapshot: bool = False):

        msg_id = self.deribit_messaging.generate_id(method)

        msg = ModelMessage(
            msg_id=msg_id,
            method=method,
            params=params
        )

        async with DeribitWebsocketConnector().get_websocket() as websocket:
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

    async def subscribe(self, subscribables: List[ModelExchangeSubscribable], snapshot: bool):

        method = "public/subscribe"

        params = {
            "channels": []
        }

        for subscribable in subscribables:
            params["channels"].append(subscribable.channel_name)
            self.subscriptions.append(subscribable)

        try:
            await self.send_instructions(method, params, snapshot)
        except Exception as e:
            print(e)
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)

    async def unsubscribe(self, subscribables: List[ModelExchangeSubscribable]):

        method = "public/unsubscribe"

        params = {
            "channels": []
        }

        for subscribable in subscribables:
            params["channels"].append(subscribable.channel_name)
            self.subscriptions.remove(subscribable)

        await self.send_instructions(method, params)