import asynctest
from deribit_arb_app.enums.enum_currency import EnumCurrency
from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull  

    ###########################################
    # TestCase Testing funcitonality of Tasks #
    ###########################################
                
class TestTasksTestCase(asynctest.TestCase):
    
    async def setUp(self):
        self.currency = EnumCurrency.BTC.value
        self.store_instrument = StoreInstruments()
        self.instrument_kind = EnumInstrumentKind.FUTURE.value
        await TaskInstrumentsPull().run(currency=self.currency, kind=self.instrument_kind)
        
    async def test(self):
        self.assertTrue(len(self.store_instrument.get_deribit_instruments()) > 0)