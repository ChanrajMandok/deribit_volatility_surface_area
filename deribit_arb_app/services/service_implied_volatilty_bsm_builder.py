import datetime
from typing import Optional

from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.services.pricers.service_pricer_black_scholes import ServicePricerBlackScholes
from deribit_arb_app.model.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility

    #################################################################
    # Service Builds implied Volatilty mesure which can be observed #
    #################################################################

class ServiceImpliedVolatilityBsmBuilder:

    # holds the indicator's logic
    # builds the indicator value using each inputs 
    
    def __init__(self, indicator_implied_volatility: ModelIndicatorBsmImpliedVolatility):
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.store_subject_index_prices = StoreSubjectIndexPrices()
        self.service_black_scholes_pricer = ServicePricerBlackScholes()
        self.instrument = indicator_implied_volatility.instrument
        self.index      = indicator_implied_volatility.index

    def build(self) -> Optional[ModelIndicatorBsmImpliedVolatility]:
        index_price = self.store_subject_index_prices.get_subject(self.index).get_instance()
        book = self.store_subject_order_books.get_subject(self.instrument).get_instance()
        name = self.instrument.instrument_name
        instrument_ask = book.best_ask_price
        instrument_bid = book.best_bid_price
        expiry_timestamp = self.instrument.expiration_timestamp
        expiry_date = datetime.datetime.utcfromtimestamp(expiry_timestamp)
        current_date = datetime.datetime.utcnow()
        
        # BSM inputs
        r = 0 
        s = index_price.price
        k = float(name.split('-')[2])
        t = (expiry_date - current_date).days / 365.0
        option_type = self.instrument.option_type
        
        target = (instrument_ask + instrument_bid) / 2 if instrument_ask and instrument_bid \
                    else instrument_ask or instrument_bid
        
        if any(not var for var in [r, s, k, t, option_type, target]):
            return None
        
        implied_vol = self.service_black_scholes_pricer.find_vol(
            target_value=target, 
            S=s, 
            K=k, 
            T=t, 
            r=0.0, 
            option_type=option_type)
        
        return ModelIndicatorBsmImpliedVolatility(
            instrument=self.instrument, 
            index=self.index,
            value=implied_vol
        )