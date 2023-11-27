import json
import traceback

from deribit_arb_app.services import logger
from deribit_arb_app.model.model_message import ModelMessage
from deribit_arb_app.model.model_subscribable import ModelSubscribable
from deribit_arb_app.services.deribit_api.service_deribit_messaging import \
                                                     ServiceDeribitMessaging
from deribit_arb_app.services.deribit_api.service_deribit_websocket_connector import \
                                                      ServiceDeribitWebsocketConnector

    ########################################################
    # Service Provides interface to Subscribe to Websocket #
    ########################################################

class ServiceDeribitSubscribe(ModelSubscribable):
    """
    Service to handle subscription and unsubscription operations with Deribit via Websocket.
    """

    def __init__(self):
        self.deribit_messaging = ServiceDeribitMessaging()
        self.subscriptions = []


    async def send_instructions(self, 
                                method: str,
                                params: dict,
                                snapshot: bool = False):
        """Send subscription or unsubscription instructions to Deribit."""

        msg_id = self.deribit_messaging.generate_id(method)

        msg = ModelMessage(msg_id=msg_id,
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
                    logger.error(f"{self.__class__.__name__}: Error: {str(e)}. Stack trace: {traceback.format_exc()}")


    async def subscribe(self, 
                        subscribables: list[ModelSubscribable],
                        snapshot: bool):
    
        """Subscribe to channels."""

        method = "public/subscribe"

        params = {
            "channels": []
        }
        
        if len(subscribables) > 1: 
            logger.info(f"{self.__class__.__name__}: {len(subscribables)} Ws Instrument Streams Subscribed")
        for subscribable in subscribables:
            params["channels"].append(subscribable.channel_name)
            if snapshot==False:
                self.subscriptions.append(subscribable)
        
        try:
            await self.send_instructions(method, params, snapshot)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. Stack trace: {traceback.format_exc()}")


    async def unsubscribe(self, unsubscribables: list[ModelSubscribable]):

        method = "public/unsubscribe"

        params = {
            "channels": []
        }
        if len(unsubscribables) > 1: 
            logger.info(f"{self.__class__.__name__}: {len(unsubscribables)} Ws Instrument Streams Unsubscribed")
        for unsubscribable in unsubscribables:
            if unsubscribable in self.subscriptions:
                self.subscriptions.remove(unsubscribable)
            params["channels"].append(unsubscribable.channel_name)
            
        await self.send_instructions(method, params)
        
        
    def get_subscriptions(self):
        subscriptions = self.subscriptions
        return subscriptions