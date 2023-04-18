import unittest

from deribit_arb_app.enums.enum_direction import EnumDirection
from deribit_arb_app.store.store_instruments import StoreInstruments

from deribit_arb_app.services.service_api_deribit import ServiceApiDeribit


class TestDeribitApiTestCase(unittest.TestCase):

    def test_api_deribit_functions(self):

        self.api_deribit = ServiceApiDeribit()
        self.store_instruments = StoreInstruments()

        self.api_deribit.get_instruments(
            currency='BTC', 
            kind='future')

        order = self.api_deribit.send_order(
            instrument=self.store_instruments.get_deribit_instrument('BTC-29DEC23'), 
            direction=EnumDirection.BUY, 
            amount=50.0, 
            price=35000.0)

        open_orders = self.api_deribit.get_open_orders(currency='BTC')

        self.assertIsNotNone(open_orders)
        self.assertIsNotNone(open_orders['BTC-29DEC23'])
        self.assertTrue(len(open_orders['BTC-29DEC23']) > 0)

        order = self.api_deribit.cancel_order(order_id=order.order_id)

        open_orders = self.api_deribit.get_open_orders(currency='BTC')

        self.assertIsNotNone(open_orders)
        self.assertIsNotNone(open_orders['BTC-29DEC23'])
        self.assertFalse(order.order_id in open_orders['BTC-29DEC23'])

        positions = self.api_deribit.get_positions(currency='BTC')

        self.assertIsNotNone(positions)
        self.assertIsNotNone(positions['BTC'])
        self.assertIsNotNone(positions['BTC']['BTC-29DEC23'])

        account_summary = self.api_deribit.get_account_summary(currency='BTC')

        self.assertIsNotNone(account_summary)
