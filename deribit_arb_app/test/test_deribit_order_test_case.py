import asyncio
import asynctest
import sys, traceback

from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.services.service_deribit_orders import ServiceDeribitOrders
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders
from deribit_arb_app.services.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe


class TestDeribitOrderTestCase(asynctest.TestCase):

    def setUp(self):
        self.instrument = ModelInstrument(instrument_name="BTC-29DEC23")
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.deribit_orders = ServiceDeribitOrders()
        self.deribit_messaging = ServiceDeribitMessaging()
        self.store_deribit_open_orders = StoreDeribitOpenOrders()
        self.my_loop = asyncio.new_event_loop()

    async def a_coroutine_order_book(self):
        await asyncio.wait_for(self.deribit_subscribe.subscribe(subscribables=[self.instrument], snapshot=True), timeout=10.0)

    async def a_coroutine_buy(self):
        try:
            price = self.store_subject_order_books.get_subject(self.instrument).get_instance().best_bid_price
            limit_price = 0.90 * price
            await asyncio.wait_for(self.deribit_orders.buy_async(
                    instrument_name=self.instrument.instrument_name, 
                    amount=50, 
                    price=limit_price), 
                timeout=3.0)
        except asyncio.TimeoutError as e:
            pass

    def test_buy(self):
        try:
            self.my_loop.run_until_complete(self.a_coroutine_order_book())
            self.my_loop.run_until_complete(self.a_coroutine_buy())
        except Exception as e:
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)
        finally:
            self.my_loop.close()
            self.assertIsNotNone(self.store_deribit_open_orders.get_deribit_open_orders(self.instrument))

    def tearDown(self):
       self.my_loop.close()