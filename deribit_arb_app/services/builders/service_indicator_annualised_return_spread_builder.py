import datetime
from typing import Optional

from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.model.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread

    #########################################################
    # Service Builds annualised spread with can be observed #
    #########################################################

class ServiceIndicatorAnnualisedReturnSpreadBuilder():

    def __init__(self):
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.store_subject_index_prices = StoreSubjectIndexPrices()

    def build(self, indicator_annualised_return_spread: ModelIndicatorAnnualisedReturnSpread) -> Optional[ModelIndicatorAnnualisedReturnSpread]:
        instrument_1 = indicator_annualised_return_spread.instrument_1
        instrument_2 = indicator_annualised_return_spread.instrument_2
        index = indicator_annualised_return_spread.index

        book1 = self.store_subject_order_books.get_subject(instrument_1).get_instance()
        book2 = self.store_subject_order_books.get_subject(instrument_2).get_instance()
        index_price = self.store_subject_index_prices.get_subject(index).get_instance()

        instrument_1_ask = book1.best_ask_price
        instrument_2_bid = book2.best_bid_price
        index_price_val = index_price.price

        if (not instrument_1_ask) or (not instrument_2_bid) or (not index_price_val):
            return None

        instrument_1_ts = instrument_1.expiration_timestamp
        instrument_2_ts = instrument_2.expiration_timestamp

        instrument_1_datetime = datetime.datetime.fromtimestamp(instrument_1_ts / 1000.0)
        instrument_2_datetime = datetime.datetime.fromtimestamp(instrument_2_ts / 1000.0)

        r2 = (instrument_2_bid / index_price_val) ** (365.0 / (instrument_2_datetime - datetime.datetime.now()).days) - 1
        r1 = (instrument_1_ask / index_price_val) ** (365.0 / (instrument_1_datetime - datetime.datetime.now()).days) - 1

        spread = r2 - r1
        amount = min(book1.best_ask_amount, book2.best_bid_amount)

        return ModelIndicatorAnnualisedReturnSpread(
            instrument_1=instrument_1,
            instrument_2=instrument_2,
            index=index,
            value=spread,
            amount=amount
        )
         


