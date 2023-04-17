import json

from deribit_arb_app.model.model_authorization import ModelAuthorization


class JsonToAuthorization:

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> ModelAuthorization:

        if 'result' not in self.json_obj:
            return ModelAuthorization()

        json_obj_result = self.json_obj['result']

        return ModelAuthorization(
            access_token=json_obj_result['access_token'],
            expires_in=json_obj_result['expires_in'],
            refresh_token=json_obj_result['refresh_token'],
            scope=json_obj_result['scope'],
            token_type=json_obj_result['token_type']
        )