import json

from deribit_arb_app.model.model_account_summary import ModelAccountSummary

    #########################################################
    # Converter Converts Json object to ModelAccountSummary #
    #########################################################

class ConverterJsonToAccountModelSummary():

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> ModelAccountSummary:

        if 'error' in self.json_obj:
            json_error = self.json_obj['error']
            if 'message' in json_error:
                json_error_message = json_error['message']
                if json_error_message == 'unauthorized':
                    return None

        json_obj_result              = self.json_obj['result']

        available_funds               = json_obj_result['available_withdrawal_funds']
        balance                       = json_obj_result['balance']
        currency                      = json_obj_result['currency']
        delta_total                   = json_obj_result['delta_total']
        equity                        = json_obj_result['equity']
        futures_pl                    = json_obj_result['futures_pl']
        options_pl                    = json_obj_result['options_pl'] 
        options_delta                 = json_obj_result['options_delta']
        options_gamma                 = json_obj_result['options_gamma']
        options_theta                 = json_obj_result['options_theta']
        options_session_rpl           = json_obj_result['options_session_rpl']
        futures_session_rpl           = json_obj_result['futures_session_rpl']
        futures_session_upl           = json_obj_result['futures_session_upl']
        margin_balance                = json_obj_result['margin_balance']
        projected_initial_margin      = json_obj_result['projected_initial_margin']
        total_pl                      = json_obj_result['total_pl']

        initial_margin                = json_obj_result['initial_margin']
        maintenance_margin            = json_obj_result['maintenance_margin']
        projected_delta_total         = json_obj_result['projected_delta_total']
        projected_maintenance_margin  = json_obj_result['projected_maintenance_margin']

        account_summary = ModelAccountSummary(
                                              available_funds              = available_funds, 
                                              balance                      = balance, 
                                              currency                     = currency, 
                                              delta_total                  = delta_total, 
                                              equity                       = equity, 
                                              futures_pl                   = futures_pl, 
                                              options_pl                   = options_pl, 
                                              options_delta                = options_delta, 
                                              options_gamma                = options_gamma, 
                                              options_theta                = options_theta, 
                                              options_session_rpl          = options_session_rpl, 
                                              futures_session_rpl          = futures_session_rpl, 
                                              futures_session_upl          = futures_session_upl, 
                                              margin_balance               = margin_balance, 
                                              projected_initial_margin     = projected_initial_margin, 
                                              total_pl                     = total_pl, 
                                              initial_margin               = initial_margin, 
                                              maintenance_margin           = maintenance_margin, 
                                              projected_delta_total        = projected_delta_total, 
                                              projected_maintenance_margin = projected_maintenance_margin, 
                                            )
        
        return account_summary