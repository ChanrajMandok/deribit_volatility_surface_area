import sys
import asyncio
import traceback
from typing import List

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.enums.enum_currency import EnumCurrency
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind
from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.model.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.store.store_subject_indicator_bsm_implied_volatilty import StoreSubjectIndicatorBsmImpliedVolatilty
from deribit_arb_app.observers.observer_indicator_bsm_implied_volatility import ObserverIndicatorBsmImpliedVolatility
from deribit_arb_app.services.retrievers.service_retrieve_deribit_liquid_option_instruments import ServiceRetrieveDeribitLiquidOptionInstruments

    ###########################################################################
    # Plot Subscribe, Observe and plot Asset Specific Volatility Surface Area #
    ###########################################################################

class ServiceImpliedVolatiltySurfaceAreaBuilder():
    
    async def setup(self):
        self.currency = EnumCurrency.BTC.value
        self.kind = EnumInstrumentKind.OPTION.value
        self.liquid_instruments_list_retriever = ServiceRetrieveDeribitLiquidOptionInstruments()
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.index = ModelIndex(index_name="btc_usd")
        self.instruments = await self.liquid_instruments_list_retriever.main(populate=False, currency=self.currency, kind=self.kind)
        self.current_observers = None
        
        observers = []
        for instrument in self.instruments:
            if instrument == self.index:
                continue
            observers.append(ModelIndicatorBsmImpliedVolatility(self,
                                                                instrument=instrument,
                                                                index=self.index
                                                                ))
        ObserverIndicatorBsmImpliedVolatility(observers)    
        
        self.store_subject_indicator_bsm_implied_volatilty = StoreSubjectIndicatorBsmImpliedVolatilty()
        self.my_loop = asyncio.new_event_loop()

    async def a_coroutine_subscribe(self, instruments:List[ModelInstrument]):
        try:
            await self.deribit_subscribe.subscribe(subscribables=instruments,
                                                   snapshot=False)
        except asyncio.exceptions.TimeoutError:
            pass
        except Exception as e:
             _, _, exc_traceback = sys.exc_info()
             traceback.print_tb(exc_traceback, limit=None, file=None)
             
    async def main(self):
        await (self.setup())
        self.instruments.insert(0,self.index)
        asyncio.create_task(await self.a_coroutine_subscribe(self.instruments))