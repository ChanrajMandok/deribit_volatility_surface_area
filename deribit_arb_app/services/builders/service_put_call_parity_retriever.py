import math
import datetime
from typing import Optional

from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.services.pricers.service_pricer_black_scholes import ServicePricerBlackScholes
from deribit_arb_app.model.indicator_models.model_indicator_put_call_parity_arbitrage import ModelIndicatorPutCallParityArbitrage

    #############################################################
    # Service Builds Put_call Parity Arbitrage relational Model #
    #############################################################

class ServiceImpliedVolatilityBsmBuilder():
    
    def __init__(self):
        self.store_subject_order_books       = StoreSubjectOrderBooks()
        self.store_subject_index_prices      = StoreSubjectIndexPrices()
        self.service_black_scholes_pricer    = ServicePricerBlackScholes()

    def build(self, indicator_put_call_parity_arbtirage: ModelIndicatorPutCallParityArbitrage) -> Optional[ModelIndicatorPutCallParityArbitrage]:
        ## instruments will already be maturity & strike matched
     
        call_instrument       = indicator_put_call_parity_arbtirage.call_instrument
        put_instrument        = indicator_put_call_parity_arbtirage.put_instrument
        index_instrument      = indicator_put_call_parity_arbtirage.index
        
        index                 = self.store_subject_index_prices.get_subject(index_instrument).get_instance()
        index_price           = index.price

        call_instrument_book  = self.store_subject_order_books.get_subject(call_instrument).get_instance()
        call_instrument_name  = call_instrument.instrument_name
        call_instrument_ask   = call_instrument_book.best_ask_price
        call_instrument_bid   = call_instrument_book.best_bid_price

        put_instrument_book   = self.store_subject_order_books.get_subject(put_instrument).get_instance()
        put_instrument_name   = put_instrument.instrument_name
        put_instrument_ask   = put_instrument_book.best_ask_price
        put_instrument_bid   = put_instrument_book.best_bid_price

        expiry_timestamp      = put_instrument.expiration_timestamp
        expiry_date           = datetime.datetime.fromtimestamp((expiry_timestamp/1000))
        current_date          = datetime.datetime.utcnow()

        ## preventing unecessary overhead of BSM calculation
        if any(not var for var in [index, index_price, call_instrument_book, put_instrument_book,
                (put_instrument_ask or put_instrument_bid),(call_instrument_ask or call_instrument_bid), expiry_date]):
            return None

        # BSM inputs
        for instrument in [call_instrument,put_instrument]     
            r = 0.0
            s = index_price
            k = float(instrument.instrument_name.split('-')[2])
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
            
            if math.isnan(implied_vol):
                # print(f"{self.instrument.instrument_name} iv is none ")
                return None

        return ModelIndicatorPutCallParityArbitrage(
            instrument=instrument, 
            index=index,
            value=implied_vol
        )
        