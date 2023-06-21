import math
import datetime

from typing import Optional

from deribit_arb_app.store.store_observable_order_books import StoreObservableOrderBooks
from deribit_arb_app.store.store_observable_index_prices import StoreObservableIndexPrices
from deribit_arb_app.services.pricers.service_pricer_black_scholes import ServicePricerBlackScholes
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import ModelIndicatorBsmImpliedVolatility

    #################################################################
    # Service Builds implied Volatility mesure which can be observed #
    #################################################################

class ServiceImpliedVolatilityBsmBuilder():
    
    def __init__(self):
        self.store_observable_order_books       = StoreObservableOrderBooks()
        self.store_observable_index_prices      = StoreObservableIndexPrices()
        self.service_black_scholes_pricer    = ServicePricerBlackScholes()

    def build(self, indicator_implied_volatility: ModelIndicatorBsmImpliedVolatility) -> Optional[ModelIndicatorBsmImpliedVolatility]:
        instrument       = indicator_implied_volatility.instrument
        index_instrument = indicator_implied_volatility.index
        index            = self.store_observable_index_prices.get_observable(index_instrument).get_instance()
        index_price      = index.price
        book             = self.store_observable_order_books.get_observable(instrument).get_instance()
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
        t = (expiry_date - current_date).total_seconds() / 31536000.0
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
        
        object_name = f"BSM Implied Volatility-{name}"
        
        return ModelIndicatorBsmImpliedVolatility(
            name=object_name,
            instrument=instrument, 
            index=index_instrument,
            implied_volatility=implied_vol,
            strike=k,
            time_to_maturity=t,
            spot=s
        )