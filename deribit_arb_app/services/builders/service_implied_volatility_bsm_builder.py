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

class ServiceImpliedVolatilityBsmBuilder:
    """
    A service builder class dedicated to constructing Black-Scholes-Merton (BSM) implied volatility indicators.
    """

    def __init__(self):
        self.store_observable_order_books      = Stores.store_observable_orderbooks
        self.store_observable_index_prices     = Stores.store_observable_index_prices
        self.store_observable_volatility_index =  Stores.store_observable_volatility_index
        self.service_black_scholes_pricer      = ServicePricerBlackScholes()

    def build(self, indicator_implied_volatility: ModelIndicatorBsmImpliedVolatility) -> Optional[ModelIndicatorBsmImpliedVolatility]:
        """
        Construct a ModelIndicatorBsmImpliedVolatility object which contains implied volatility data.
        """
        # Extract the necessary attributes from the indicator_implied_volatility object
        instrument = indicator_implied_volatility.instrument
        index_instrument = indicator_implied_volatility.index
        hvol_instrument = indicator_implied_volatility.volatility_index
        
        # Get the current price of the index instrument
        index = self.store_observable_index_prices.get_observable(index_instrument).get_instance()
        index_price = index.price if hasattr(index, 'price') else None
        
        # Get the current volatility index value
        volatility_index = self.store_observable_volatility_index.get_observable(hvol_instrument).get_instance()
        dvol_value = volatility_index.volatility if hasattr(volatility_index, 'volatility') else None
        
        # Get details from the order book for the instrument
        book = self.store_observable_order_books.get_observable(instrument).get_instance()
        instrument_name = instrument.name if hasattr(instrument, 'name') else None
        instrument_ask = book.best_ask_price if hasattr(book, 'best_ask_price') else None
        instrument_bid = book.best_bid_price if hasattr(book, 'best_bid_price') else None
        
        # Extract the expiration timestamp and determine the option type based on the instrument name
        expiry_timestamp = instrument.expiration_timestamp if hasattr(instrument, 'expiration_timestamp') else None
        option_type = EnumOptionType.CALL if instrument_name.rstrip()[-1] == 'C' else EnumOptionType.PUT
        expiry_date = datetime.fromtimestamp((expiry_timestamp/1000))
        current_date = datetime.utcnow()
        
        # Return None if any of the necessary attributes are missing or invalid
        if any(not var for var in [index, index_price, book, instrument_name, dvol_value, (instrument_ask or instrument_bid), expiry_date]):
            return None

        # BSM model input parameters
        r = 0.0  # Risk-free rate
        s = index_price  # Spot price of the underlying asset
        k = float(instrument_name.split('-')[2])  # Strike price
        t = (expiry_date - current_date).total_seconds() / 31536000.0  # Time to expiration (in years)
        
        # Scaled Dvol value as initial best guess
        h = min(dvol_value * np.sqrt(t / 30), 2)

        # Calculate the average price if both bid and ask prices are available, otherwise use available one
        target_in_ccy = (instrument_ask + instrument_bid) / 2 if instrument_ask and instrument_bid else instrument_ask or instrument_bid
        target = target_in_ccy * s
        
        # Calculate the implied volatility using Black-Scholes model
        implied_vol = self.service_black_scholes_pricer.find_vol(
            target_value=target, 
            S=s, 
            K=k, 
            T=t, 
            r=r, 
            h=h,
            option_type=option_type
        )
        
        # Return None if the calculated implied volatility is not valid
        if math.isnan(implied_vol) or implied_vol < 0:
            return None
        
        # Construct the name for the output object
        object_name = f"BSM Implied Volatility-{instrument_name}"
        
        # Return the constructed ModelIndicatorBsmImpliedVolatility instance with all the relevant details
        model_indicator_bsm_implied_volatility = \
                 ModelIndicatorBsmImpliedVolatility(spot=s,
                                                    strike=k,
                                                    name=object_name,
                                                    time_to_maturity=t,
                                                    instrument=instrument, 
                                                    timestamp=current_date,
                                                    index=index_instrument,
                                                    option_type=option_type,
                                                    implied_volatility=implied_vol
                                                   )
        
        return model_indicator_bsm_implied_volatility