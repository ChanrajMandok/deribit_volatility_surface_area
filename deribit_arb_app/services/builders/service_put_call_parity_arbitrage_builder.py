import math

from typing import Optional
from datetime import datetime

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.services.pricers.service_pricer_black_scholes import \
                                                  ServicePricerBlackScholes
from deribit_arb_app.model.indicator_models.model_indicator_put_call_parity_arbitrage import \
                                                             ModelIndicatorPutCallVolArbitrage

    #############################################################
    # Service Builds Put_call Parity Arbitrage relational Model #
    #############################################################

class ServicePutCallParityAribtrageBuilder:
    
    def __init__(self):
        self.service_black_scholes_pricer    = ServicePricerBlackScholes()
        self.store_observable_order_books = Stores.store_observable_orderbooks
        self.store_observable_index_prices = Stores.store_observable_index_prices
        

    def build(self, 
              indicator_put_call_parity_arbtirage: ModelIndicatorPutCallVolArbitrage) -> Optional[ModelIndicatorPutCallVolArbitrage]:
        ## instruments will already be maturity & strike matched

        ## not completed
     
        call_instrument       = indicator_put_call_parity_arbtirage.call_instrument
        put_instrument        = indicator_put_call_parity_arbtirage.put_instrument
        index_instrument      = indicator_put_call_parity_arbtirage.index
        
        index                 = self.store_observable_index_prices.get(index_instrument).get_instance()
        index_price           = index.price

        call_instrument_book  = self.store_observable_order_books.get(call_instrument).get_instance()
        call_instrument_name  = call_instrument.name
        call_instrument_ask   = call_instrument_book.best_ask_price
        call_instrument_bid   = call_instrument_book.best_bid_price

        put_instrument_book   = self.store_observable_order_books.get(put_instrument).get_instance()
        put_instrument_name   = put_instrument.name
        put_instrument_ask    = put_instrument_book.best_ask_price
        put_instrument_bid    = put_instrument_book.best_bid_price

        expiry_timestamp      = put_instrument.expiration_timestamp
        expiry_date           = datetime.fromtimestamp((expiry_timestamp/1000))
        current_date          = datetime.utcnow()

        ## preventing unecessary overhead of BSM calculation
        if any(not var for var in [index, index_price, call_instrument_book, put_instrument_book,
                (put_instrument_ask or put_instrument_bid),(call_instrument_ask or call_instrument_bid), expiry_date]):
            return None
        
        k = float(call_instrument.name.split('-')[2])
        t = (expiry_date - current_date).days / 365.0
        r = 0.0

        call_target = (call_instrument_ask + call_instrument_bid) / 2 if call_instrument_ask and call_instrument_bid \
                    else call_instrument_ask or call_instrument_bid
            
        call_implied_vol = self.service_black_scholes_pricer.find_vol(
            target_value=call_target, 
            S=index_price, 
            K=k, 
            T=t, 
            r=r, 
            option_type=call_instrument.option_type)
        
        put_target = (put_instrument_ask + put_instrument_bid) / 2 if put_instrument_ask and put_instrument_bid \
                    else put_instrument_ask or put_instrument_bid
            
        put_implied_vol = self.service_black_scholes_pricer.find_vol(
            target_value=put_target, 
            S=index_price, 
            K=k, 
            T=t, 
            r=r, 
            option_type=put_instrument.option_type)

        if math.isnan(call_implied_vol) or math.isnan(put_implied_vol):
            # print(f"{self.instrument.name} iv is none ")
            return None
        
        # Calculate present value of strike price
        pvk = k * math.exp(-r * t)

        # Calculate put-call parity difference
        # put_call_parity_diff = call_value + pvk - put_value - S
        # arbitrage = abs(put_call_parity_diff) > threshold  # replace 'threshold' with an appropriate value

        return ModelIndicatorPutCallVolArbitrage(
            put_instrument=put_instrument, 
            call_instrument=call_instrument,
            index=index,
            value=put_call_parity_diff,
            arbitrage=arbitrage
        )
        