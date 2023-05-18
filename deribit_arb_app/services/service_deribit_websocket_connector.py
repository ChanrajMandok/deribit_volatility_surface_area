import os
import websockets
from singleton_decorator import singleton

    #############################################
    # Service Connects to Deribit via Websocket #
    #############################################

@singleton
class ServiceDeribitWebsocketConnector():

    def __init__(self):

        self.base_ws = os.environ['BASE_WS_URL']
        self.websocket = websockets.connect(self.base_ws)

    async def __aenter__(self):
        self.websocket = await websockets.connect(self.base_ws)
        return self.websocket

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.websocket.close()
