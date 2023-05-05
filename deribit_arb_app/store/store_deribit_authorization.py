from typing import Optional
from singleton_decorator import singleton

from deribit_arb_app.model.model_authorization import ModelAuthorization

    ################################################
    # Store Manages & Stores Derebit Authorization #
    ################################################

@singleton
class StoreDeribitAuthorization:

    def __init__(self):
        self.__authorization = None

    def set_authorization(self, authorization: ModelAuthorization):
        self.__authorization = authorization

    def get_authorization(self) -> Optional[ModelAuthorization]:
        return self.__authorization

    def is_authorized(self) -> bool:
        return (not self.__authorization.access_token is None)