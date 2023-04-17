from typing import Dict


class ModelMessage:

    def __init__(self,
                 msg_id: int,
                 method: str,
                 params: Dict = None,
                 jsonrpc="2.0"
                 ):

        self.jsonrpc = jsonrpc
        self.id = msg_id
        self.method = method

        if params is None:
            self.params = {}
        else:
            self.params = params

    def build_message(self) -> Dict:

        return {
                "jsonrpc": self.jsonrpc,
                "id": self.id,
                "method": self.method,
                "params": self.params
            }