import os
import websockets
from singleton_decorator import singleton

    #############################################
    # Service Connects to Deribit via Websocket #
    #############################################

@singleton
class ServiceDeribitWebsocketConnector:

    def __init__(self):

        self.base_ws = os.environ['BASE_WS_URL']
        self.websocket = websockets.connect(self.base_ws)

    def get_websocket(self):
        return self.websocket
