from typing import Optional
import datetime

from deribit_arb_app.model.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks


class IndicatorAnnualisedReturnSpreadBuilder:

    # holds the indicator's logic
    # builds the indicator value using the relevant order books
    
    def __init__(self, indicator_annualised_return_spread: ModelIndicatorAnnualisedReturnSpread):
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.store_subject_index_prices = StoreSubjectIndexPrices()
        self.instrument1 = indicator_annualised_return_spread.instrument1
        self.instrument2 = indicator_annualised_return_spread.instrument2
        self.index = indicator_annualised_return_spread.index

    def build(self) -> Optional[ModelIndicatorAnnualisedReturnSpread]:
        book1 = self.store_subject_order_books.get_subject(self.instrument1).get_instance()
        book2 = self.store_subject_order_books.get_subject(self.instrument2).get_instance()
        index_price = self.store_subject_index_prices.get_subject(self.index).get_instance()
        instrument1_ask = book1.best_ask_price
        instrument2_bid = book2.best_bid_price
        index_price_val = index_price.price

        if (not instrument1_ask) or (not instrument2_bid) or (not index_price_val):
            return None 

        instrument1_ts = self.instrument1.expiration_timestamp
        instrument2_ts = self.instrument2.expiration_timestamp

        instrument1_datetime = datetime.datetime.fromtimestamp(instrument1_ts/1000.0)
        instrument2_datetime = datetime.datetime.fromtimestamp(instrument2_ts/1000.0)

        r2 = (instrument2_bid / index_price_val)**(365.0 / (instrument2_datetime - datetime.datetime.now()).days) - 1
        r1 = (instrument1_ask / index_price_val)**(365.0 / (instrument1_datetime - datetime.datetime.now()).days) - 1

        spread = r2 - r1
        amount = min(book1.best_ask_amount, book2.best_bid_amount)

        return ModelIndicatorAnnualisedReturnSpread(
            instrument1=self.instrument1,
            instrument2=self.instrument2,
            index=self.index,
            value=spread,
            amount=amount
        )
         


