import json

from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.converters.json_to_authorization import JsonToAuthorization
from deribit_arb_app.store.store_deribit_authorization import StoreDeribitAuthorization


@Singleton
class DeribitAuthenticationHandler:

    def __init__(self):

        self.authorization = None

    def set_authorization(self, result):

        json_to_authorization = JsonToAuthorization(json.dumps(result))
        authorization = json_to_authorization.convert()
        StoreDeribitAuthorization().set_authorization(authorization)
