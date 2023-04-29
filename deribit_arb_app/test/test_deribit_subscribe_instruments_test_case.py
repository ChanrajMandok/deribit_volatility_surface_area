import sys
import asyncio
import traceback
import asynctest

from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentPull

from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.services.service_api_deribit import ServiceApiDeribit
from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe


    ##########################################################################
    # TestCase Testing funcitonality to subscribe to Instrument Price Stream #
    ##########################################################################

class TestDeribitSubscribeInstrumentsTestCase(asynctest.TestCase):

    async def setUp(self):
        super().setUp()
        await TaskInstrumentPull().run()
        self.store_instrument = StoreInstruments()
        self.instrument = self.store_instrument.get_deribit_instrument('BTC-PERPETUAL')
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.my_loop = asyncio.new_event_loop()
        self.deribit_api = ServiceApiDeribit()
        
    async def a_coroutine_subscribe(self):
        try:
            await asyncio.wait_for(self.deribit_subscribe.subscribe(
                    subscribables=[self.instrument], snapshot=False), timeout=10)
        except asyncio.exceptions.TimeoutError:
            pass
        except Exception as e:
             _, _, exc_traceback = sys.exc_info()
             traceback.print_tb(exc_traceback, limit=None, file=None)
             
    async def a_coroutine_unsubscribe(self):
        await self.deribit_subscribe.unsubscribe([self.instrument], snapshot=False)


    def test_subscribe(self):
        try:
            self.my_loop.run_until_complete(self.a_coroutine_subscribe())
        finally:
            self.my_loop.close()