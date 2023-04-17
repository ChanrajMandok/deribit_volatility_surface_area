from typing import Optional
from deribit_arb_app.model.model_account_summary import ModelAccountSummary
from deribit_arb_app.store.store_deribit_account_summary import StoreDeribitAccountSummary
import json

from singleton_pattern_decorator.decorator import Singleton

from deribit_arb_app.converters.json_to_account_summary import JsonToAccountSummary


@Singleton
class DeribitAccountSummaryHandler:

    def __init__(self):

        self.store_deribit_account_summary = StoreDeribitAccountSummary()
        self.account_summary = None
        
    def set_account_summary(self, result) -> Optional[ModelAccountSummary]:

        self.account_summary = JsonToAccountSummary(json.dumps(result)).convert()
        account_summary = self.store_deribit_account_summary.set_deribit_account_summary(self.account_summary)
        return account_summary

