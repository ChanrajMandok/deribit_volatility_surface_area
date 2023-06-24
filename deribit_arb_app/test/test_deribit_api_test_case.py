import unittest

from deribit_arb_app.store.stores import Stores 
from deribit_arb_app.enums.enum_currency import EnumCurrency
from deribit_arb_app.enums.enum_direction import EnumDirection
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind
from deribit_arb_app.services.deribit_api.service_api_deribit import ServiceApiDeribit

    ##############################################
    # TestCase Service Deribit API Functionality #
    ##############################################

class TestDeribitApiTestCase(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        super().setUp()
        self.api_deribit = ServiceApiDeribit()
        self.store_subscribable_instruments = Stores.store_subscribable_instruments
        
        self.currency = EnumCurrency.BTC.value
        self.instrument_kind = EnumInstrumentKind.FUTURE.value
        self.instrument = 'BTC-PERPETUAL'

    async def test_api_deribit_functions(self):

        await self.api_deribit.get_instruments(
            currency=self.currency, 
            kind=self.instrument_kind)
        
        self.assertIsNotNone(self.store_subscribable_instruments.get_subscribables)
        
        #Check price is below the market price, else order will be instantly filled
        order = await self.api_deribit.send_order(
                        instrument=self.store_subscribable_instruments.get_subscribable_via_key(self.instrument), 
                        direction=EnumDirection.BUY, 
                        amount=50.0, 
                        price=25000)

        open_orders = await self.api_deribit.get_open_orders(currency=self.currency)

        self.assertIsNotNone(open_orders)
        self.assertIsNotNone(open_orders.get(self.instrument))
        self.assertTrue(len(open_orders.get(self.instrument, [])) > 0)

        order = await self.api_deribit.cancel_order(order_id=order.order_id)

        open_orders = await self.api_deribit.get_open_orders(currency=self.currency)

        self.assertTrue(len(open_orders.get(self.instrument, [])) == 0)
        self.assertNotIn(order.order_id, open_orders.get(self.instrument, []))

        positions = await self.api_deribit.get_positions(currency=self.currency)

        self.assertIsNotNone(positions)
        self.assertIsNotNone(positions.get(self.currency))
        self.assertIsNotNone(positions.get(self.currency).get(self.instrument))

        account_summary = await self.api_deribit.get_account_summary(currency=self.currency)

        self.assertIsNotNone(account_summary)