import math
import numpy as np

from typing import Optional
from datetime import datetime

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.enums.enum_option_type import EnumOptionType
from deribit_arb_app.services.pricers.service_pricer_black_scholes import \
                                                  ServicePricerBlackScholes
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import \
                                                         ModelIndicatorBsmImpliedVolatility
                                                         
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
        
        instrument           = indicator_implied_volatility.instrument
        index_instrument     = indicator_implied_volatility.index
        hvol_instrument      = indicator_implied_volatility.volatility_index
        index                = self.store_observable_index_prices.get_observable(index_instrument).get_instance()
        index_price          = index.price if hasattr(index, 'price') else None
        volatility_index     = self.store_observable_volatility_index.get_observable(hvol_instrument).get_instance()
        hvol_value           = volatility_index.volatility if hasattr(volatility_index, 'volatility') else None
        book                 = self.store_observable_order_books.get_observable(instrument).get_instance()
        instrument_name      = instrument.name if hasattr(instrument, 'name') else None
        instrument_ask       = book.best_ask_price if hasattr(book, 'best_ask_price') else None
        instrument_bid       = book.best_bid_price if hasattr(book, 'best_bid_price') else None
        expiry_timestamp     = instrument.expiration_timestamp if hasattr(instrument, 'expiration_timestamp') else None
        option_type          = EnumOptionType.CALL if instrument_name.rstrip()[-1] == 'C' else EnumOptionType.PUT
        expiry_date          = datetime.fromtimestamp((expiry_timestamp/1000))
        current_date         = datetime.utcnow()
    
        ## preventing unecessary overhead of BSM calculation
        if any(not var for var in [index, index_price, book, instrument_name, hvol_value, (instrument_ask or instrument_bid), expiry_date]):
            return None

        # BSM inputs
        r = 0.0
        s = index_price
        k = float(instrument_name.split('-')[2])
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
        
        object_name = f"BSM Implied Volatility-{instrument_name}"
        
        return ModelIndicatorBsmImpliedVolatility(
            spot=s,
            strike=k,
            name=object_name,
            time_to_maturity=t,
            instrument=instrument, 
            timestamp=current_date,
            index=index_instrument,
            option_type=option_type,
            implied_volatility=implied_vol
        )