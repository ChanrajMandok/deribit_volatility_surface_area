from typing import Optional
from datetime import datetime

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.indicator_models.model_indicator_annualised_return_spread import \
                                                         ModelIndicatorAnnualisedReturnSpread

    #########################################################
    # Service Builds annualised spread with can be observed #
    #########################################################

class ServiceIndicatorAnnualisedReturnSpreadBuilder:
    """
    Service class to build the annualized return spread indicator for given instruments and index.
    
    The annualized return spread is calculated between two instruments based on their respective prices 
    and the price of an index.
    """

    def __init__(self):
        self.store_observable_order_books = Stores.store_observable_orderbooks
        self.store_observable_index_prices = Stores.store_observable_index_prices

    def build(self, indicator_annualised_return_spread: ModelIndicatorAnnualisedReturnSpread) -> Optional[ModelIndicatorAnnualisedReturnSpread]:
        """Builds the annualized return spread indicator."""
        # Extracting the instruments and index from the input indicator.
        instrument_1 = indicator_annualised_return_spread.instrument_1
        instrument_2 = indicator_annualised_return_spread.instrument_2
        index = indicator_annualised_return_spread.index

        # Getting the order book instances for both instruments.
        book1 = self.store_observable_order_books.get_observable(instrument_1).get_instance()
        book2 = self.store_observable_order_books.get_observable(instrument_2).get_instance()
        # Getting the index price instance.
        index_price = self.store_observable_index_prices.get_observable(index).get_instance()

        # Retrieving best ask price for instrument 1 and best bid price for instrument 2.
        # If they don't exist, default to None.
        instrument_1_ask = getattr(book1, 'best_ask_price', None)
        instrument_2_bid = getattr(book2, 'best_bid_price', None)
        # Retrieving the price for the index.
        index_price_val = getattr(index_price, 'price', None)

        # If any of the above prices is missing, we cannot compute the spread.
        if not all([instrument_1_ask, instrument_2_bid, index_price_val]):
            return None

        # Extracting expiration timestamps for both instruments.
        instrument_1_ts = instrument_1.expiration_timestamp
        instrument_2_ts = instrument_2.expiration_timestamp

        # Converting the timestamps to datetime objects for easier arithmetic.
        instrument_1_datetime = datetime.fromtimestamp(instrument_1_ts / 1000.0)
        instrument_2_datetime = datetime.fromtimestamp(instrument_2_ts / 1000.0)

        # Calculating the annualized returns for both instruments.
        r2 = (instrument_2_bid / index_price_val) ** (365.0 / (instrument_2_datetime - datetime.now()).days) - 1
        r1 = (instrument_1_ask / index_price_val) ** (365.0 / (instrument_1_datetime - datetime.now()).days) - 1

        # The spread is the difference between the returns of instrument 2 and instrument 1.
        spread = r2 - r1
        # The amount is the minimum between the best ask amount of book1 and the best bid amount of book2.
        amount = min(book1.best_ask_amount, book2.best_bid_amount)

        # Returning a new ModelIndicatorAnnualisedReturnSpread with the computed values.
        model_indicator_annualised_return_spread = \
                ModelIndicatorAnnualisedReturnSpread(
                                                    instrument_1=instrument_1,
                                                    instrument_2=instrument_2,
                                                    index=index,
                                                    value=spread,
                                                    amount=amount
                                                )
        
        return model_indicator_annualised_return_spread