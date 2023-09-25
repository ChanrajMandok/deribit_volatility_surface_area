import json

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_authorization import ModelAuthorization

    ########################################################
    # Converter Converts Json object to ModelAuthorization #
    ########################################################

class ConverterJsonToModelAuthorization():

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> ModelAuthorization:

        if 'result' not in self.json_obj:
            return ModelAuthorization()

        json_obj_result     = self.json_obj['result']

        try:
            a = ModelAuthorization(
                access_token   =json_obj_result['access_token'],
                expires_in     =json_obj_result['expires_in'],
                refresh_token  =json_obj_result['refresh_token'],
                scope          =json_obj_result['scope'],
                token_type     =json_obj_result['token_type']
            )

        except Exception as e:
            logger.error(f"{self.__class__.__name__}: {e}")

        return a 