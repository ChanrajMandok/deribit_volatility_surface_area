import json

from decimal import Decimal

from deribit_arb_app.model.model_subscribable_instrument import \
                                        ModelSubscribableInstrument

    #############################################################
    # Converter Converts Json object to list of ModelInstrument #
    #############################################################

class ConverterJsonToInstruments():

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> list[ModelSubscribableInstrument]:

        instruments = []

        json_obj_result = self.json_obj['result']

        for json_instrument in json_obj_result:

            tick_size             = Decimal(json_instrument['tick_size'])
            taker_commission      = Decimal(json_instrument['taker_commission'])
            settlement_period     = str(json_instrument['settlement_period'])
            quote_currency        = str(json_instrument['quote_currency'])

            option_type = None
            if 'option_type' in json_instrument:
                option_type       = json_instrument['option_type']

            min_trade_amount      =  Decimal(json_instrument['min_trade_amount'])
            maker_commission      =  Decimal(json_instrument['maker_commission'])

            max_leverage = None
            if 'max_leverage' in json_instrument:
                max_leverage       = int(json_instrument['max_leverage'])

            kind                   = json_instrument['kind']
            is_active              = json_instrument['is_active']
            instrument_name        = json_instrument['instrument_name']
            expiration_timestamp   = json_instrument['expiration_timestamp']
            creation_timestamp     = json_instrument['creation_timestamp']
            contract_size          = json_instrument['contract_size']
            base_currency          = json_instrument['base_currency']

            instruments.append(
                ModelSubscribableInstrument(
                tick_size                = tick_size,
                taker_commission         = taker_commission,
                settlement_period        = settlement_period,
                quote_currency           = quote_currency,
                option_type              = option_type,
                min_trade_amount         = min_trade_amount,
                maker_commission         = maker_commission,
                max_leverage             = max_leverage,
                kind                     = kind,
                is_active                = is_active,
                name                     = instrument_name,
                expiration_timestamp     = expiration_timestamp,
                creation_timestamp       = creation_timestamp,
                contract_size            = contract_size,
                base_currency            = base_currency
                                                ))

        return instruments