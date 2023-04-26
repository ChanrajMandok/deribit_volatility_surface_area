import asyncio
import asynctest
import sys, traceback

from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.enums.enum_direction import EnumDirection
from deribit_arb_app.services.service_api_deribit import ServiceApiDeribit

from deribit_arb_app.services.service_deribit_orders import ServiceDeribitOrders
from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders
from deribit_arb_app.services.service_deribit_messaging import ServiceDeribitMessaging

class TestDeribitOrderCancelOpenOrderTestCase(asynctest.TestCase):

    def setUp(self):
        self.deribit_orders = ServiceDeribitOrders()
        self.api_deribit = ServiceApiDeribit()
        self.deribit_messaging = ServiceDeribitMessaging()
        self.store_deribit_open_orders = StoreDeribitOpenOrders()
        self.instrument = ModelInstrument("BTC-PERPETUAL")
        self.open_order_id = None
      
    async def a_coroutine_get_open_orders(self):
        await asyncio.wait_for(self.deribit_orders.get_open_orders_by_currency('BTC'),timeout=100.0)
    
    async def a_coroutine_cancel(self):
        
        order = self.api_deribit.send_order(
                        instrument=self.store_instruments.get_deribit_instrument(self.instument), 
                        direction=EnumDirection.BUY, 
                        amount=50.0, 
                        price=24000)

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
            self.loop.run_until_complete(self.a_coroutine_get_open_orders())
            self.loop.run_until_complete(self.a_coroutine_cancel())
            self.loop.run_until_complete(self.a_coroutine_get_open_orders())
        except Exception as e:
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)
        finally:
            self.loop.close()
            self.assertIsNone(self.store_deribit_open_orders.get_deribit_open_order(self.instrument, self.open_order_id ))
            
