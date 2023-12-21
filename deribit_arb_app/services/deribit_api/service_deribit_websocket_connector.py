import os
import ssl
import certifi
import websockets

from singleton_decorator import singleton

    #############################################
    # Service Connects to Deribit via Websocket #
    #############################################

@singleton
class ServiceDeribitWebsocketConnector():
    """
    A singleton class to manage the Deribit Websocket connection.
    """

    def __init__(self):
        self.base_ws = os.environ.get('BASE_WS_URL', None)
        self.websocket = websockets.connect(self.base_ws)

    async def __aenter__(self):
        """
        Async context manager entry point to establish a websocket connection.

        Returns:
        - WebSocketClientProtocol: An established websocket connection.
        """

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.websocket = await websockets.connect(self.base_ws, ssl=ssl_context)
        return self.websocket

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit point to close the websocket connection.
        """
        await self.websocket.close()