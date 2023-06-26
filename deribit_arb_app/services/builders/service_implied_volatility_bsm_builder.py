import math
import datetime
import numpy as np 
from typing import Optional

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.services.pricers.service_pricer_black_scholes import ServicePricerBlackScholes
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import ModelIndicatorBsmImpliedVolatility

    ##################################################################
    # Service Builds implied Volatility mesure which can be observed #
    ##################################################################

class ServiceImpliedVolatilityBsmBuilder():
    
    def __init__(self):
        self.store_observable_order_books      = Stores.store_observable_orderbooks
        self.store_observable_index_prices     = Stores.store_observable_index_prices
        self.store_observable_volatility_index =  Stores.store_observable_volatility_index
        self.service_black_scholes_pricer      = ServicePricerBlackScholes()

    def build(self, indicator_implied_volatility: ModelIndicatorBsmImpliedVolatility) -> Optional[ModelIndicatorBsmImpliedVolatility]:
        instrument       = indicator_implied_volatility.instrument
        index_instrument = indicator_implied_volatility.index
        hvol_instrument  = indicator_implied_volatility.volatility_index
        index            = self.store_observable_index_prices.get_observable(index_instrument).get_instance()
        index_price      = index.price if hasattr(index, 'price') else None
        volatility_index = self.store_observable_volatility_index.get_observable(hvol_instrument).get_instance()
        hvol_value       = volatility_index.volatility if hasattr(volatility_index, 'volatility') else None
        book             = self.store_observable_order_books.get_observable(instrument).get_instance()
        instument_name   = instrument.name if hasattr(instrument, 'name') else None
        instrument_ask   = book.best_ask_price if hasattr(book, 'best_ask_price') else None
        instrument_bid   = book.best_bid_price if hasattr(book, 'best_bid_price') else None
        expiry_timestamp = instrument.expiration_timestamp if hasattr(instrument, 'expiration_timestamp') else None
        expiry_date      = datetime.datetime.fromtimestamp((expiry_timestamp/1000))
        current_date     = datetime.datetime.utcnow()

        ## preventing unecessary overhead of BSM calculation
        if any(not var for var in [index, index_price, book, instument_name, hvol_value, (instrument_ask or instrument_bid), expiry_date]):
            return None

        # BSM inputs
        r = 0.0
        s = index_price
        k = float(instument_name.split('-')[2])
        t = (expiry_date - current_date).total_seconds() / 31536000.0
        option_type = instrument.option_type
        h = min(hvol_value * np.sqrt(t / 30), 2)

        target_in_ccy = (instrument_ask + instrument_bid) / 2 if instrument_ask and instrument_bid \
                    else instrument_ask or instrument_bid
        
        target = target_in_ccy*s
            
        implied_vol = self.service_black_scholes_pricer.find_vol(
            target_value=target, 
            S=s, 
            K=k, 
            T=t, 
            r=r, 
            h=h,
            option_type=option_type)
        
        if math.isnan(implied_vol) or implied_vol < 0:
            # print(f"{self.instument_name} iv is none ")
            return None
        
        object_name = f"BSM Implied Volatility-{instument_name}"
        
        return ModelIndicatorBsmImpliedVolatility(
            name=object_name,
            instrument=instrument, 
            index=index_instrument,
            implied_volatility=implied_vol,
            strike=k,
            time_to_maturity=t,
            spot=s
        )