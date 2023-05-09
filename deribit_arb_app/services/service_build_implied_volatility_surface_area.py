import sys
import asyncio
import traceback
from typing import List

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.model.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.store.store_subject_indicator_bsm_implied_volatilty import StoreSubjectIndicatorBsmImpliedVolatilty
from deribit_arb_app.observers.observer_indicator_bsm_implied_volatility import ObserverIndicatorBsmImpliedVolatility
from deribit_arb_app.services.retrievers.service_retrieve_deribit_liquid_option_instruments import ServiceRetrieveDeribitLiquidOptionInstruments

    ###########################################################################
    # Plot Subscribe, Observe and plot Asset Specific Volatility Surface Area #
    ###########################################################################

class ServiceBuildVolatiltySurfaceArea():
    
    async def setup(self):
        self.liquid_instruments_list_retriever = ServiceRetrieveDeribitLiquidOptionInstruments()
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.index = ModelIndex(index_name="btc_usd")
        self.instruments = await self.liquid_instruments_list_retriever.main()
        # self.observer_indicator_bsm_implied_volatility = ObserverIndicatorBsmImpliedVolatility() 
        
        observers = []
        for instrument in self.instruments:
            observers.append(ModelIndicatorBsmImpliedVolatility(self,
                                                            instrument=instrument,
                                                            index=self.index
                                                            ))
        ObserverIndicatorBsmImpliedVolatility(observers)    
        
        self.store_subject_indicator_bsm_implied_volatilty = StoreSubjectIndicatorBsmImpliedVolatilty()
        self.my_loop = asyncio.new_event_loop()

    async def a_coroutine_subscribe(self, instruments:List):
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
