import math
import datetime

from typing import Optional

from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.services.pricers.service_pricer_black_scholes import ServicePricerBlackScholes
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility

    #################################################################
    # Service Builds implied Volatilty mesure which can be observed #
    #################################################################

class ServiceImpliedVolatilityBsmBuilder():
    
    def __init__(self):
        self.store_subject_order_books       = StoreSubjectOrderBooks()
        self.store_subject_index_prices      = StoreSubjectIndexPrices()
        self.service_black_scholes_pricer    = ServicePricerBlackScholes()

    def build(self, indicator_implied_volatility: ModelIndicatorBsmImpliedVolatility) -> Optional[ModelIndicatorBsmImpliedVolatility]:
        instrument       = indicator_implied_volatility.instrument
        index_instrument = indicator_implied_volatility.index
        
        index            = self.store_subject_index_prices.get_subject(index_instrument).get_instance()
        index_price      = index.price
        book             = self.store_subject_order_books.get_subject(instrument).get_instance()
        name             = instrument.instrument_name
        instrument_ask   = book.best_ask_price
        instrument_bid   = book.best_bid_price
        expiry_timestamp = instrument.expiration_timestamp
        expiry_date      = datetime.datetime.fromtimestamp((expiry_timestamp/1000))
        current_date     = datetime.datetime.utcnow()

        ## preventing unecessary overhead of BSM calculation
        if any(not var for var in [index, index_price, book, name, (instrument_ask or instrument_bid), expiry_date]):
            return None

        # BSM inputs
        r = 0.0
        s = index_price
        k = float(name.split('-')[2])
        t = (expiry_date - current_date).days / 365.0
        option_type = instrument.option_type
        
        target = (instrument_ask + instrument_bid) / 2 if instrument_ask and instrument_bid \
                    else instrument_ask or instrument_bid
            
        implied_vol = self.service_black_scholes_pricer.find_vol(
            target_value=target, 
            S=s, 
            K=k, 
            T=t, 
            r=r, 
            option_type=option_type)
        
        if math.isnan(implied_vol) or implied_vol < 0:
            # print(f"{self.instrument.instrument_name} iv is none ")
            return None

        return ModelIndicatorBsmImpliedVolatility(
            instrument=instrument, 
            index=index_instrument,
            value=implied_vol
        )
        