import json

from singleton_decorator import singleton
from deribit_arb_app.store.store_deribit_authorization import StoreDeribitAuthorization
from deribit_arb_app.converters.converter_json_to_authorization import ConverterJsonToAuthorization

    ##########################################
    # Service Handels Deribit Authentication #
    ##########################################

@singleton
class ServiceDeribitAuthenticationHandler:

    def __init__(self):

        self.authorization = None

    def set_authorization(self, result):

        json_to_authorization = ConverterJsonToAuthorization(json.dumps(result))
        authorization = json_to_authorization.convert()
        StoreDeribitAuthorization().set_authorization(authorization)
