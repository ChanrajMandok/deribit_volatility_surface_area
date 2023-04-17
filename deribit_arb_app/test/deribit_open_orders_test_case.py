
import asyncio
import asynctest
import sys, traceback

from deribit_arb_app.services.deribit_orders import DeribitOrders
from deribit_arb_app.services.deribit_messaging import DeribitMessaging
from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders
from deribit_arb_app.model.model_instrument import ModelInstrument


class DeribitOpenOrdersTestCase(asynctest.TestCase):

    def setUp(self):
        self.store_deribit_open_orders = StoreDeribitOpenOrders()
        self.deribit_orders = DeribitOrders()
        self.deribit_messaging = DeribitMessaging()
        self.instrument = ModelInstrument(instrument_name="BTC-29DEC23")
        self.my_loop = asyncio.new_event_loop()

    async def a_coroutine(self):
        await asyncio.wait_for(self.deribit_orders.get_open_orders_by_currency(currency="BTC"), timeout=100.0)

    def test_get_open_orders_by_currency(self):
        try:
            self.my_loop.run_until_complete(self.a_coroutine())
        except Exception as e:
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)
        finally:
            self.my_loop.close()
            self.assertIsNotNone(self.store_deribit_open_orders.get_deribit_open_orders(instrument=self.instrument))

    def tearDown(self):
       self.my_loop.close()