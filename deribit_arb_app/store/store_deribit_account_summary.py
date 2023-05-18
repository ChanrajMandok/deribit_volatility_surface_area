from typing import Optional
from singleton_decorator import singleton

from deribit_arb_app.model.model_account_summary import ModelAccountSummary

    ##################################################
    # Store Manages & stores Derebit Account Summary #
    ##################################################

@singleton
class StoreDeribitAccountSummary():

    def __init__(self):
        self.__account_summary = None

    def set_deribit_account_summary(self, account_summary: ModelAccountSummary) -> Optional[ModelAccountSummary]:
        self.__account_summary = account_summary
        return self.__account_summary

    def get_deribit_account_summary(self) -> Optional[ModelAccountSummary]:
        return self.__account_summary
