import asyncio
import unittest
import sys, traceback

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.enums.enum_currency import EnumCurrency
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull
from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders
from deribit_arb_app.services.deribit_api.service_api_deribit import ServiceApiDeribit
from deribit_arb_app.services.deribit_api.service_deribit_orders import ServiceDeribitOrders
from deribit_arb_app.services.deribit_api.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.services.deribit_api.service_deribit_messaging import ServiceDeribitMessaging

    #################################################
    # TestCase esting DeribitOrders Functionalities #
    #################################################

class TestDeribitAllOrderOperationsTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.currency = EnumCurrency.BTC.value
        self.instrument_kind = EnumInstrumentKind.FUTURE.value
        await TaskInstrumentsPull().run(currency=self.currency, kind=self.instrument_kind)
        self.store_subscribable_instrument = Stores.store_subscribable_instruments
        self.instrument = self.store_subscribable_instrument.get_subscribable_via_key('BTC-PERPETUAL')
        self.deribit_api = ServiceApiDeribit()
        self.store_observable_order_books = Stores.store_observable_orderbooks
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.deribit_orders = ServiceDeribitOrders()
        self.deribit_messaging = ServiceDeribitMessaging()
        self.store_deribit_open_orders = StoreDeribitOpenOrders()
        self.open_order_id = None

    async def a_coroutine_order_book(self):
        await asyncio.wait_for(self.deribit_subscribe.subscribe(subscribables=[self.instrument], snapshot=True), timeout=25.0)

    async def a_coroutine_buy(self):
        price = self.store_observable_order_books.get_observable(self.instrument).get_instance().best_bid_price
        limit_price = round(0.98 * price,0)
        
        await self.deribit_orders.buy_async(
                instrument_name=self.instrument.name, 
                amount=(float(self.instrument.contract_size*10)), 
                price=limit_price)
    
    async def a_coroutine_get_open_orders(self):
        await asyncio.wait_for(self.deribit_orders.get_open_orders_by_currency(self.currency),timeout=10.0)

    async def a_coroutine_cancel_all(self):

        open_orders = self.store_deribit_open_orders.get_deribit_open_orders(self.instrument)
        if open_orders is None:
            raise ValueError('there are no open_orders in the store dictionary!')
        try:
            await asyncio.wait_for(self.deribit_orders.cancel_all(),timeout=15.0)
        except asyncio.TimeoutError as e:
            pass

    async def a_coroutine_cancel(self):

        open_orders = self.store_deribit_open_orders.get_deribit_open_orders(self.instrument)
        if open_orders is None:
            raise ValueError('there are no open_orders in the store dictionary!')
        self.open_order_id = list(open_orders.keys())[0]
        try:
            await asyncio.wait_for(self.deribit_orders.cancel(order_id=self.open_order_id),timeout=3.0)
        except asyncio.TimeoutError as e:
            pass

    async def test_orders_operations(self):
        try:
            # Test order book, buying, and getting open orders
            await self.a_coroutine_order_book()
            await self.a_coroutine_buy()
            await self.a_coroutine_get_open_orders()

            # Test cancelling a single order
            await self.a_coroutine_cancel()
            await self.a_coroutine_get_open_orders()
            self.assertIsNone(self.store_deribit_open_orders.get_deribit_open_order(self.instrument, self.open_order_id ))

            # Buy again to test cancelling all orders
            await self.a_coroutine_buy()
            await self.a_coroutine_get_open_orders()

            # Test cancelling all orders
            await self.a_coroutine_cancel_all()
            await self.a_coroutine_get_open_orders()
            self.assertIsNone(self.store_deribit_open_orders.get_deribit_open_orders(self.instrument))
        except Exception as e:
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)
