import asyncio
import asynctest
import sys, traceback

from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.enums.enum_currency import EnumCurrency
from deribit_arb_app.store.store_instruments import StoreInstruments
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull
from deribit_arb_app.services.service_deribit_subscribe import ServiceDeribitSubscribe
from deribit_arb_app.observers.observer_indicator_annualised_return_spread import ObserverIndicatorAnnualisedReturnSpread
from deribit_arb_app.model.indicator_models.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread
from deribit_arb_app.store.store_subject_indicator_annualized_return_spreads import StoreSubjectIndicatorAnnualizedReturnSpreads

    #########################################################################################################
    # TestCase Testing funcitonality to calculate aned subscribe to internally calculated Annualised Spread #
    #########################################################################################################

class TestDeribitIndicatorAnnualizedReturnSpreadBuilderTestCase(asynctest.TestCase):

    async def setUp(self):
        self.currency = EnumCurrency.BTC.value
        self.instrument_kind = EnumInstrumentKind.FUTURE.value
        await TaskInstrumentsPull().run(currency=self.currency, kind=self.instrument_kind)
        self.store_instrument = StoreInstruments()
        self.instrument_1 = self.store_instrument.get_deribit_instrument('BTC-29SEP23')
        self.instrument_2 = self.store_instrument.get_deribit_instrument('BTC-29DEC23')
        
        self.index = ModelIndex(EnumIndexCurrency.BTC.value)
        
        self.deribit_subscribe = ServiceDeribitSubscribe()
        
        # create an instance of ObserverIndicatorAnnualisedReturnSpread
        self.observer_indicator_annualised_return_spread = ObserverIndicatorAnnualisedReturnSpread()
        
        # create an instance of ModelIndicatorAnnualisedReturnSpread
        indicator = ModelIndicatorAnnualisedReturnSpread(self,
                                                         instrument_1 = self.instrument_1,
                                                         instrument_2 = self.instrument_2,
                                                         index = self.index)
        # add the indicator to the observer
        self.observer_indicator_annualised_return_spread.attach_indicator(indicator)
        
        self.store_subject_indicator_annualized_return_spreads = StoreSubjectIndicatorAnnualizedReturnSpreads()
        self.my_loop = asyncio.new_event_loop()

    async def a_coroutine(self):
        try:
            await asyncio.wait_for(self.deribit_subscribe.subscribe(
                        subscribables=[
                            self.instrument_1,
                            self.instrument_2,
                            self.index],
                            snapshot=False), timeout=10) 
        except asyncio.TimeoutError as e:
            pass
        except Exception as e:
             _, _, exc_traceback = sys.exc_info()
             traceback.print_tb(exc_traceback, limit=None, file=None)

    def test_subscribe(self):
        try:
            self.my_loop.run_until_complete(self.a_coroutine())
        finally:
            self.my_loop.close()