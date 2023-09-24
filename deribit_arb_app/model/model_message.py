from django.db import models

    #############################
    # Model for Message Objects #
    #############################

class ModelMessage(models.Model):

    def __init__(self,
                 msg_id: int,
                 method: str,
                 params: dict = None,
                 jsonrpc="2.0"
                 ):

        self.jsonrpc = jsonrpc
        self.id = msg_id
        self.method = method

        if params is None:
            self.params = {}
        else:
            self.params = params

    def build_message(self) -> dict:

        return {
                "jsonrpc": self.jsonrpc,
                "id": self.id,
                "method": self.method,
                "params": self.params
            }