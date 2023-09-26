
from typing import Optional
from datetime import datetime

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.indicator_models.model_indicator_annualised_return_spread import \
                                                         ModelIndicatorAnnualisedReturnSpread

    #########################################################
    # Service Builds annualised spread with can be observed #
    #########################################################

class ServiceIndicatorAnnualisedReturnSpreadBuilder():

    def __init__(self):
        self.store_observable_order_books = Stores.store_observable_orderbooks
        self.store_observable_index_prices = Stores.store_observable_index_prices

    def build(self, indicator_annualised_return_spread: ModelIndicatorAnnualisedReturnSpread) -> Optional[ModelIndicatorAnnualisedReturnSpread]:
        instrument_1 = indicator_annualised_return_spread.instrument_1
        instrument_2 = indicator_annualised_return_spread.instrument_2
        index = indicator_annualised_return_spread.index

        book1 = self.store_observable_order_books.get_observable(instrument_1).get_instance()
        book2 = self.store_observable_order_books.get_observable(instrument_2).get_instance()
        index_price = self.store_observable_index_prices.get_observable(index).get_instance()

        instrument_1_ask = book1.best_ask_price  if hasattr(book1, 'best_ask_price') else None
        instrument_2_bid = book2.best_bid_price if hasattr(book2, 'best_bid_price') else None
        index_price_val = index_price.price if hasattr(index_price, 'price') else None

        if (not instrument_1_ask) or (not instrument_2_bid) or (not index_price_val):
            return None

        instrument_1_ts = instrument_1.expiration_timestamp
        instrument_2_ts = instrument_2.expiration_timestamp

        instrument_1_datetime = datetime.fromtimestamp(instrument_1_ts / 1000.0)
        instrument_2_datetime = datetime.fromtimestamp(instrument_2_ts / 1000.0)

        r2 = (instrument_2_bid / index_price_val) ** (365.0 / (instrument_2_datetime - datetime.now()).days) - 1
        r1 = (instrument_1_ask / index_price_val) ** (365.0 / (instrument_1_datetime - datetime.now()).days) - 1

        spread = r2 - r1
        amount = min(book1.best_ask_amount, book2.best_bid_amount)

        return ModelIndicatorAnnualisedReturnSpread(
            instrument_1=instrument_1,
            instrument_2=instrument_2,
            index=index,
            value=spread,
            amount=amount
        )
         


