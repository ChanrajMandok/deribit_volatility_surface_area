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
    """
    Singleton class to manage and handle Deribit authorization data.
    """

    def __init__(self):
        self.store_authorization = Stores.store_model_authorization
        self.authorization = None


    def set_authorization(self, result):
        """
        Process and store the provided authorization data.
        """
        json_to_authorization = ConverterJsonToModelAuthorization(json.dumps(result))
        authorization = json_to_authorization.convert()
        self.store_authorization.set(authorization)
