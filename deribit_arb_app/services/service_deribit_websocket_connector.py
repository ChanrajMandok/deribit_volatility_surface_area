import websockets
from singleton_decorator import singleton

    #############################################
    # Service Connects to Deribit via Websocket #
    #############################################

@singleton
class ServiceDeribitWebsocketConnector:

    def __init__(self):

        self.url = "wss://www.deribit.com/ws/api/v2"
        self.websocket = websockets.connect(self.url)

    def get_websocket(self):
        return self.websocket
