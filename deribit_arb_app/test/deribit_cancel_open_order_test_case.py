import traceback
import asyncio
import asynctest
import sys, traceback

from deribit_arb_app.services.deribit_orders import DeribitOrders
from deribit_arb_app.services.deribit_messaging import DeribitMessaging
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders


class DeribitOrderCancelOpenOrderTestCase(asynctest.TestCase):

    def setUp(self):
        self.deribit_orders = DeribitOrders()
        self.deribit_messaging = DeribitMessaging()
        self.store_deribit_open_orders = StoreDeribitOpenOrders()
        self.instrument = ModelInstrument("BTC-29DEC23")
        self.my_loop = asyncio.new_event_loop()
        self.open_order_id = None
      
    async def a_coroutine_get_open_orders(self):
        await asyncio.wait_for(self.deribit_orders.get_open_orders_by_currency('BTC'),timeout=100.0)

    async def a_coroutine_cancel(self):

        open_orders = self.store_deribit_open_orders.get_deribit_open_orders(self.instrument)
        if open_orders is None:
            raise ValueError('there are no open_orders in the store dictionary!')
        self.open_order_id = list(open_orders.keys())[0]

        try:
            await asyncio.wait_for(self.deribit_orders.cancel(order_id=self.open_order_id),timeout=3.0)
        except asyncio.TimeoutError as e:
            pass

    def test_cancel_open_order(self):
        try:
            self.my_loop.run_until_complete(self.a_coroutine_get_open_orders())
            self.my_loop.run_until_complete(self.a_coroutine_cancel())
            self.my_loop.run_until_complete(self.a_coroutine_get_open_orders())
        except Exception as e:
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)
        finally:
            self.my_loop.close()
            self.assertIsNone(self.store_deribit_open_orders.get_deribit_open_order(self.instrument, self.open_order_id ))
            
