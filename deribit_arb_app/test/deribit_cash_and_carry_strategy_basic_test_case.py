import asyncio
import unittest
import time

from deribit_arb_app.observers.observer_strategy_cash_and_carry_basic import ObserverStrategyCashAndCarryBasic
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentPull
from deribit_arb_app.services.api_deribit import ApiDeribit
from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.strategies.strategy_cash_and_carry_basic import StrategyCashAndCarryBasic


class DeribitCashAndCarryStrategyBasicTestCase(unittest.TestCase):

    def setUp(self):

        self.api_deribit = ApiDeribit()
        self.store_instruments = StoreInstruments()

        # get instruments

        TaskInstrumentPull().run()

        # subscribing to prices

        self.instrument1 = self.store_instruments.get_deribit_instrument('BTC-29DEC23')
        self.instrument2 = self.store_instruments.get_deribit_instrument('BTC-25MAR22')
        self.index = ModelIndex(
            index_name="btc_usd"
        )

        # running the strategy

        self.strategy_cash_and_carry_basic = StrategyCashAndCarryBasic(
            instrument1 = self.instrument1, 
            instrument2 = self.instrument2, 
            index = self.index
        )

        self.observer_strategy_cash_and_carry_basic = ObserverStrategyCashAndCarryBasic(
            instance=self.strategy_cash_and_carry_basic
        )

    def test_run(self):
        self.my_loop = asyncio.get_event_loop()
        self.my_loop.run_until_complete(
            self.api_deribit.subscribe([
                self.instrument1, self.instrument2, self.index
            ])
        )
