import asyncio
import asynctest
import sys, traceback

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentPull
from deribit_arb_app.model.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread

from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.observers.observer_indicator_annualised_return_spread import ObserverIndicatorAnnualisedReturnSpread


class TestDeribitIndicatorAnnualizedReturnSpreadBuilderTestCase(asynctest.TestCase):

    async def setUp(self):
        await TaskInstrumentPull().run()
        self.store_instrument = StoreInstruments()
        self.instrument_1 = self.store_instrument.get_deribit_instrument('BTC-29SEP23')
        self.instrument_2 = self.store_instrument.get_deribit_instrument('BTC-29DEC23')
        
        self.index = ModelIndex(
            index_name="btc_usd")
        
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.observer_indicator_annualised_return_spread = ObserverIndicatorAnnualisedReturnSpread(
            ModelIndicatorAnnualisedReturnSpread(self,
                instrument_1 = self.instrument_1,
                instrument_2 = self.instrument_2,
                index = self.index))
        
        self.my_loop = asyncio.new_event_loop()

    async def a_coroutine(self):
        try:
            await asyncio.wait_for(self.deribit_subscribe.subscribe(
                        subscribables=[
                            self.instrument_1,
                            self.instrument_2,
                            self.index
                        ]
            ), timeout=15) 
        except asyncio.TimeoutError as e:
            pass
        except Exception as e:
             _, _, exc_traceback = sys.exc_info()
             traceback.print_tb(exc_traceback, limit=None, file=None)

    def test_subscribe(self):
        try:
            self.my_loop.run_until_complete(self.a_coroutine())
        finally:
            self.my_loop.close()

    def tearDown(self):
       self.my_loop.close()