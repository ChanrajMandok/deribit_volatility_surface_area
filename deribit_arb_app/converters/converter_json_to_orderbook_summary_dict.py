import json

from decimal import Decimal

from deribit_arb_app.converters import logger
from deribit_arb_app.model.model_orderbook_summary import ModelOrderbookSummary

    ############################################################
    # Converter Converts Json object to Orderbook Summary Dict #
    ############################################################

class ConverterJsonToOrderbookSummaryDict:
    """
    Converter class for transforming a JSON string representing order book summaries into 
    a list of ModelOrderbookSummary instances.
    """
    
    def __init__(self, json_string: str):
        self.json_obj = json.loads(json_string)

    def convert(self) -> list[ModelOrderbookSummary]:
        """Converts the internal JSON object into a list of ModelOrderbookSummary instances. """

        try:
            if not self.json_obj or 'result' not in self.json_obj:
                logger.warning("Invalid JSON format: Missing 'result' field.")
                return []

            json_obj_result = self.json_obj['result']

            if not isinstance(json_obj_result, list):
                logger.warning("Expected a list of orderbook summaries.")
                return []

            orderbook_summary = [
                ModelOrderbookSummary(
                    volume_usd=Decimal(str(item.get('volume_usd', ''))) if item.get('volume_usd') else None,
                    volume=Decimal(str(item.get('volume', ''))) if item.get('volume') else None,
                    underlying_price=Decimal(str(item.get('underlying_price', ''))) if item.get('underlying_price') else None,
                    underlying_index=item.get('underlying_index'),
                    quote_currency=item.get('quote_currency'),
                    price_change=Decimal(str(item.get('price_change', ''))) if item.get('price_change') else None,
                    open_interest=Decimal(str(item.get('open_interest', ''))) if item.get('open_interest') else None,
                    mid_price=Decimal(str(item.get('mid_price', ''))) if item.get('mid_price') else None,
                    mark_price=Decimal(str(item.get('mark_price', ''))) if item.get('mark_price') else None,
                    low=Decimal(str(item.get('low', ''))) if item.get('low') else None,
                    last=Decimal(str(item.get('last', ''))) if item.get('last') else None,
                    interest_rate=Decimal(str(item.get('interest_rate', ''))) if item.get('interest_rate') else None,
                    instrument_name=item.get('instrument_name'),
                    high=Decimal(str(item.get('high', ''))) if item.get('high') else None,
                    estimated_delivery_price=Decimal(str(item.get('estimated_delivery_price', ''))) if item.get('estimated_delivery_price') else None,
                    creation_timestamp=item.get('creation_timestamp'),
                    bid_price=Decimal(str(item.get('bid_price', ''))) if item.get('bid_price') else None,
                    base_currency=item.get('base_currency'),
                    ask_price=Decimal(str(item.get('ask_price', ''))) if item.get('ask_price') else None
                )
                for item in json_obj_result
            ]

            return orderbook_summary
        
        except Exception as e:
            logger.error(f"An error occurred during conversion in {self.__class__.__name__}: {e}")
            return []