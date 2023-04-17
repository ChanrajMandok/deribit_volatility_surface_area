import websockets
from singleton_pattern_decorator.decorator import Singleton


@Singleton
class DeribitWebsocketConnector:

    def __init__(self):

        self.url = "wss://www.deribit.com/ws/api/v2"
        self.websocket = websockets.connect(self.url)

    def get_websocket(self):
        return self.websocket
