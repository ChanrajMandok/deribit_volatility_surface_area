import sys
import asyncio
import unittest
import traceback

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.enums.enum_currency import EnumCurrency
from deribit_arb_app.enums.enum_volatility_index_currency import \
                                       EnumVolatilityIndexCurrency
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency
from deribit_arb_app.services.deribit_api.service_api_deribit import \
                                                     ServiceApiDeribit
from deribit_arb_app.model.model_subscribable_volatility_index import \
                                       ModelSubscribableVolatilityIndex
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull
from deribit_arb_app.services.deribit_api.service_deribit_subscribe import \
                                                     ServiceDeribitSubscribe
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
    ##########################################################################
    # TestCase Testing funcitonality to subscribe to Instrument Price Stream #
    ##########################################################################

class TestDeribitSubscribeInstrumentsTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.currency = EnumCurrency.BTC.value
        self.instrument_kind = EnumInstrumentKind.FUTURE.value
        await TaskInstrumentsPull().run(currency=self.currency, kind=self.instrument_kind)
        self.store_subscribable_instrument = Stores.store_subscribable_instruments
        self.instrument = self.store_subscribable_instrument.get_via_key('BTC-PERPETUAL')
        self.index = ModelSubscribableIndex(name=EnumIndexCurrency.BTC.value)
        self.vol = ModelSubscribableVolatilityIndex(name=EnumVolatilityIndexCurrency.BTC.value)
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.deribit_api = ServiceApiDeribit()
        
    async def a_coroutine_subscribe(self):
        try:
            await asyncio.wait_for(self.deribit_subscribe.subscribe(
                    subscribables=[self.index, self.instrument ,self.vol], snapshot=False), timeout=10)
        except asyncio.exceptions.TimeoutError:
            pass
        except Exception as e:
             _, _, exc_traceback = sys.exc_info()
             traceback.print_tb(exc_traceback, limit=None, file=None)
             
    async def a_coroutine_unsubscribe(self):
        await self.deribit_subscribe.unsubscribe([self.instrument], snapshot=False)

    async def test_subscribe(self):
        await self.a_coroutine_subscribe()