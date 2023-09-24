import json

from typing import Optional
from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_account_summary import ModelAccountSummary
from deribit_arb_app.converters.converter_json_to_account_model_summary import \
                                              ConverterJsonToAccountModelSummary

    ##############################################
    # Service Implements Account Summary Handler #
    ##############################################

@singleton
class ServiceDeribitAccountSummaryHandler():

    def __init__(self):

        self.store_deribit_account_summary = Stores.store_model_account_summary
        self.account_summary = None
        
    def set_account_summary(self, result) -> Optional[ModelAccountSummary]:

        self.account_summary = ConverterJsonToAccountModelSummary(json.dumps(result)).convert()
        account_summary = self.store_deribit_account_summary.set(self.account_summary)
        return account_summary

