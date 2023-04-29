import asyncio
import asynctest
import sys, traceback

from deribit_arb_app.services.service_api_deribit import ServiceApiDeribit

from deribit_arb_app.services.service_deribit_orders import ServiceDeribitOrders
from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders
from deribit_arb_app.services.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull

    ###########################################################
    # TestCase Testing DeribitOrders Cancel All Functionality #
    ###########################################################

class TestDeribitOrderCancelAllOpenOrderTestCase(asynctest.TestCase):

    async def setUp(self):
        super().setUp()
        await TaskInstrumentsPull().run()
        self.store_instrument = StoreInstruments()
        self.instrument = self.store_instrument.get_deribit_instrument('BTC-PERPETUAL')
        self.deribit_api = ServiceApiDeribit()
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.deribit_orders = ServiceDeribitOrders()
        self.deribit_messaging = ServiceDeribitMessaging()
        self.store_deribit_open_orders = StoreDeribitOpenOrders()
        self.my_loop = asyncio.new_event_loop()
        self.open_order_id = None
    
    async def a_coroutine_order_book(self):
        await asyncio.wait_for(self.deribit_subscribe.subscribe(subscribables=[self.instrument], snapshot=True), timeout=25.0)

    async def a_coroutine_buy(self):
        price = self.store_subject_order_books.get_subject(self.instrument).get_instance().best_bid_price
        limit_price = round(0.98 * price,0)
        
        await self.deribit_orders.buy_async(
                instrument_name=self.instrument.instrument_name, 
                amount=(float(self.instrument.contract_size*10)), 
                price=limit_price)
    
    async def a_coroutine_get_open_orders(self):
        await asyncio.wait_for(self.deribit_orders.get_open_orders_by_currency('BTC'),timeout=10.0)

    async def a_coroutine_cancel_all(self):

        open_orders = self.store_deribit_open_orders.get_deribit_open_orders(self.instrument)
        if open_orders is None:
            raise ValueError('there are no open_orders in the store dictionary!')
        try:
            await asyncio.wait_for(self.deribit_orders.cancel_all(),timeout=15.0)
        except asyncio.TimeoutError as e:
            pass

    def test_cancel_open_order(self):
        try:
            self.my_loop.run_until_complete(self.a_coroutine_order_book())
            self.my_loop.run_until_complete(self.a_coroutine_buy())
            self.my_loop.run_until_complete(self.a_coroutine_get_open_orders())
            self.my_loop.run_until_complete(self.a_coroutine_cancel_all())
            self.my_loop.run_until_complete(self.a_coroutine_get_open_orders())
        except Exception as e:
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)
        finally:
            self.my_loop.close()
            self.assertIsNone(self.store_deribit_open_orders.get_deribit_open_orders(self.instrument))