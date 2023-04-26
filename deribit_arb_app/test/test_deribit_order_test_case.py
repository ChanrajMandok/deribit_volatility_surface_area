import asyncio
import asynctest
import sys, traceback

from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_deribit_open_orders import StoreDeribitOpenOrders

from deribit_arb_app.services.service_api_deribit import ServiceApiDeribit
from deribit_arb_app.services.service_deribit_orders import ServiceDeribitOrders
from deribit_arb_app.services.service_deribit_messaging import ServiceDeribitMessaging
from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe


    #######################################################################
    # TestCase Testing Authentication Object in StoreDeribitAuthorization #
    #######################################################################
    
class TestDeribitOrderTestCase(asynctest.TestCase):

    def setUp(self):
        self.store_instrument = StoreInstruments()
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.deribit_subscribe = ServiceDeribitSubscribe()
        self.deribit_orders = ServiceDeribitOrders()
        self.deribit_messaging = ServiceDeribitMessaging()
        self.store_deribit_open_orders = StoreDeribitOpenOrders()
        self.deribit_api = ServiceApiDeribit()
        self.my_loop = asyncio.new_event_loop()
        self.instrument = None
        
    async def a_corountine_get_instruments(self):
        await asyncio.wait_for(self.deribit_api.get_instruments(currency='BTC', kind='future'), timeout=25)
        self.instrument = self.store_instrument.get_deribit_instrument('BTC-PERPETUAL')

    async def a_coroutine_order_book(self):
        await asyncio.wait_for(self.deribit_subscribe.subscribe(subscribables=[self.instrument], snapshot=True), timeout=25.0)

    async def a_coroutine_buy(self):
        price = self.store_subject_order_books.get_subject(self.instrument).get_instance().best_bid_price
        limit_price = round(0.98 * price,0)
        
        await self.deribit_orders.buy_async(
                instrument_name=self.instrument.instrument_name, 
                amount=(float(self.instrument.contract_size*10)), 
                price=limit_price)
        
    def test_buy(self):
        try: 
            self.my_loop.run_until_complete(self.a_corountine_get_instruments())
            self.my_loop.run_until_complete(self.a_coroutine_order_book())
            self.my_loop.run_until_complete(self.a_coroutine_buy())
        except Exception as e:
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)
        finally:
            self.my_loop.close()
            self.assertIsNotNone(self.store_deribit_open_orders.get_deribit_open_orders(self.instrument))