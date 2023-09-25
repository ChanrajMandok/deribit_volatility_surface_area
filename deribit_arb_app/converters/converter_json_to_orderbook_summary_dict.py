import json

from decimal import Decimal

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_orderbook_summary import ModelOrderbookSummary

    ############################################################
    # Converter Converts Json object to Orderbook Summary Dict #
    ############################################################

class ConverterJsonToOrderbookSummaryDict():

    def __init__(self, json_string):

        self.json_obj = json.loads(json_string)

    def convert(self) -> dict:

        try:
            json_obj_result = self.json_obj['result']

            orderbook_summary = [
                   ModelOrderbookSummary(
                        volume_usd               = Decimal(str(dict_value.get('volume_usd'))) if dict_value.get('volume_usd') else None,
                        volume                   = Decimal(str(dict_value.get('volume'))) if dict_value.get('volume') else None,
                        underlying_price         = Decimal(str(dict_value.get('underlying_price'))) if dict_value.get('underlying_price') else None,
                        underlying_index         = dict_value.get('underlying_index'),
                        quote_currency           = dict_value.get('quote_currency'),
                        price_change             = Decimal(str(dict_value.get('price_change'))) if dict_value.get('price_change') else None,
                        open_interest            = Decimal(str(dict_value.get('open_interest'))) if dict_value.get('open_interest') else None,
                        mid_price                = Decimal(str(dict_value.get('mid_price'))) if dict_value.get('mid_price') else None,
                        mark_price               = Decimal(str(dict_value.get('mark_price'))) if dict_value.get('mark_price') else None,
                        low                      = Decimal(str(dict_value.get('low'))) if dict_value.get('low') else None,
                        last                     = Decimal(str(dict_value.get('last'))) if dict_value.get('last') else None,
                        interest_rate            = Decimal(str(dict_value.get('interest_rate'))) if dict_value.get('interest_rate') else None,
                        instrument_name          = dict_value.get('instrument_name'),
                        high                     = Decimal(str(dict_value.get('high'))) if dict_value.get('high') else None,
                        estimated_delivery_price = Decimal(str(dict_value.get('estimated_delivery_price'))) if dict_value.get('estimated_delivery_price') else None,
                        creation_timestamp       = dict_value.get('creation_timestamp'),
                        bid_price                = Decimal(str(dict_value.get('bid_price'))) if dict_value.get('bid_price') else None,
                        base_currency            = dict_value.get('base_currency'),
                        ask_price                = Decimal(str(dict_value.get('ask_price'))) if dict_value.get('ask_price') else None
                    )
                for dict_value in json_obj_result
                                 ]

            return orderbook_summary
        
        except Exception as e:
            logger.error(f"An error occurred during conversion: {self.__class__.__name__} {e}")