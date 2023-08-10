import unittest
from deribit_arb_app.store.stores import Stores
from deribit_arb_app.enums.enum_currency import EnumCurrency
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull  

    ###########################################
    # TestCase Testing funcitonality of Tasks #
    ###########################################
                
class TestTasksTestCase(unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp(self):
        self.currency = EnumCurrency.BTC.value
        self.store_subscribable_instrument = Stores.store_subscribable_instruments
        self.instrument_kind = EnumInstrumentKind.FUTURE.value
        await TaskInstrumentsPull().run(currency=self.currency, kind=self.instrument_kind)
        
    async def test_subscribables_length(self):
        self.assertTrue(len(self.store_subscribable_instrument.get_subscribables()) > 0)