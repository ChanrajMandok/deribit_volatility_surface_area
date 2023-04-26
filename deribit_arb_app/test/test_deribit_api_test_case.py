import asynctest

from deribit_arb_app.enums.enum_direction import EnumDirection
from deribit_arb_app.store.store_instruments import StoreInstruments

from deribit_arb_app.services.service_api_deribit import ServiceApiDeribit

    ######################################
    # TestCase Deribit ApI Functionality #
    ######################################

class TestDeribitApiTestCase(asynctest.TestCase):

    def setUp(self):
        super().setUp
        self.api_deribit = ServiceApiDeribit()
        self.store_instruments = StoreInstruments()
        
        self.currency = 'BTC'
        self.instument_type = 'future'
        self.instument = 'BTC-29DEC23'

    async def test_api_deribit_functions(self):

        await self.api_deribit.get_instruments(
            currency=self.currency, 
            kind=self.instument_type)
        
        self.assertIsNotNone(self.store_instruments.get_deribit_instruments())
        
        #Check price is below the market price, else order will be instantly filled
        order = await self.api_deribit.send_order(
                        instrument=self.store_instruments.get_deribit_instrument(self.instument), 
                        direction=EnumDirection.BUY, 
                        amount=50.0, 
                        price=24000)

        open_orders = await self.api_deribit.get_open_orders(currency=self.currency)

        self.assertIsNotNone(open_orders)
        self.assertIsNotNone(open_orders[self.instument])
        self.assertTrue(len(open_orders[self.instument]) > 0)

        order = await self.api_deribit.cancel_order(order_id=order.order_id)

        open_orders = await self.api_deribit.get_open_orders(currency=self.currency)

        self.assertIsNotNone(open_orders)
        self.assertIsNotNone(open_orders[self.instument])
        self.assertFalse(order.order_id in open_orders[self.instument])

        positions = await self.api_deribit.get_positions(currency=self.currency)

        self.assertIsNotNone(positions)
        self.assertIsNotNone(positions[self.currency])
        self.assertIsNotNone(positions[self.currency][self.instument])

        account_summary = await self.api_deribit.get_account_summary(currency=self.currency)

        self.assertIsNotNone(account_summary)
