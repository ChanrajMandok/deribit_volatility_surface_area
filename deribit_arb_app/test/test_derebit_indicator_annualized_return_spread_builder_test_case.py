import asyncio
import asynctest
import sys, traceback

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.model.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread

from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.observers.observer_indicator_annualised_return_spread import ObserverIndicatorAnnualisedReturnSpread


class TestDeribitIndicatorAnnualizedReturnSpreadBuilderTestCase(asynctest.TestCase):

    def setUp(self):
        self.instrument1 = ModelInstrument(
            instrument_name="BTC-29SEP23",
            expiration_timestamp=1632488400000
            )
        self.instrument2 = ModelInstrument(
            instrument_name="BTC-29DEC23",
            expiration_timestamp=1640955600000
            )
        self.index = ModelIndex(
            index_name="btc_usd"
        )
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.observer_indicator_annualised_return_spread = ObserverIndicatorAnnualisedReturnSpread(
            ModelIndicatorAnnualisedReturnSpread(self.instrument1, self.instrument2, self.index)
        )
        self.my_loop = asyncio.new_event_loop()

    async def a_coroutine(self):
        try:
            await asyncio.wait_for(self.deribit_subscribe.subscribe(
                        subscribables=[
                            self.instrument1,
                            self.instrument2,
                            self.index
                        ]
            ), timeout=3.0) 
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