import json

from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.converters.converter_json_to_model_authorization import \
                                             ConverterJsonToModelAuthorization

    ##########################################
    # Service Handels Deribit Authentication #
    ##########################################

@singleton
class ServiceDeribitAuthenticationHandler():

    def __init__(self):
        self.store_authorization = Stores.store_model_authorization
        self.authorization = None

    def set_authorization(self, result):

        json_to_authorization = ConverterJsonToModelAuthorization(json.dumps(result))
        authorization = json_to_authorization.convert()
        self.store_authorization.set(authorization)
