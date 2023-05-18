import asyncio
import asynctest
import sys, traceback

from deribit_arb_app.enums.enum_currency import EnumCurrency
from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind
from deribit_arb_app.services.service_api_deribit import ServiceApiDeribit
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull
from deribit_arb_app.services.service_deribit_orders import ServiceDeribitOrders
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders
from deribit_arb_app.services.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe

    ################################################################################################
    # TestCase Testing Orderbook Snapshot and Deribit Orders Buy & Cancel & Retrieve Functionality #
    ################################################################################################
    
class TestDeribitOrderOpenCloseTestCase(asynctest.TestCase):

    async def setUp(self):
        super().setUp()
        self.currency = EnumCurrency.BTC.value
        self.instrument_kind = EnumInstrumentKind.FUTURE.value
        await TaskInstrumentsPull().run(currency=self.currency, kind=self.instrument_kind)
        self.store_instrument = StoreInstruments()
        self.instrument = self.store_instrument.get_deribit_instrument('BTC-PERPETUAL')
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.deribit_orders = ServiceDeribitOrders()
        self.deribit_messaging = ServiceDeribitMessaging()
        self.store_deribit_open_orders = StoreDeribitOpenOrders()
        self.deribit_api = ServiceApiDeribit()
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
        await asyncio.wait_for(self.deribit_orders.get_open_orders_by_currency(EnumCurrency.BTC.value),timeout=25.0)
        
    async def a_coroutine_cancel(self):

        open_orders = self.store_deribit_open_orders.get_deribit_open_orders(self.instrument)
        if open_orders is None:
            raise ValueError('there are no open_orders in the store dictionary!')
        self.open_order_id = list(open_orders.keys())[0]
        try:
            await asyncio.wait_for(self.deribit_orders.cancel(order_id=self.open_order_id),timeout=3.0)
        except asyncio.TimeoutError as e:
            pass

    def test_buy_and_cancel_open_order(self):
        try: 
            self.my_loop.run_until_complete(self.a_coroutine_order_book())
            self.my_loop.run_until_complete(self.a_coroutine_buy())
            self.assertIsNotNone(self.store_deribit_open_orders.get_deribit_open_orders(instrument=self.instrument))
            
            self.my_loop.run_until_complete(self.a_coroutine_get_open_orders())
            self.my_loop.run_until_complete(self.a_coroutine_cancel())
            self.my_loop.run_until_complete(self.a_coroutine_get_open_orders())
            self.assertIsNone(self.store_deribit_open_orders.get_deribit_open_order(self.instrument, self.open_order_id ))
            
        except Exception as e:
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)
        finally:
            
            self.my_loop.close()