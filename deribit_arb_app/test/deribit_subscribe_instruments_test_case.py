import sys
import traceback
import asynctest
import asyncio

from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.services.deribit_subscribe import DeribitSubscribe


class DeribitSubscribeInstrumentsTestCase(asynctest.TestCase):

    def setUp(self):
        self.deribit_subscribe = DeribitSubscribe()
        self.my_loop = asyncio.new_event_loop()

    async def a_coroutine(self):
        
        try:
            await asyncio.wait_for(self.deribit_subscribe.subscribe(
                    subscribables=[
                        ModelInstrument(
                            instrument_name="BTC-29SEP23"
                        )
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
