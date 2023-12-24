import asyncio
import unittest
import sys, traceback

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.enums.enum_currency import EnumCurrency
from deribit_arb_app.enums.enum_index_currency import EnumIndexCurrency
from deribit_arb_app.enums.enum_instrument_kind import EnumInstrumentKind
from deribit_arb_app.tasks.task_instruments_pull import TaskInstrumentsPull
from deribit_arb_app.services.deribit_api.service_deribit_subscribe import \
                                                     ServiceDeribitSubscribe
from deribit_arb_app.model.model_subscribable_index import ModelSubscribableIndex
from deribit_arb_app.observers.observer_indicator_annualised_return_spread import \
                                            ObserverIndicatorAnnualisedReturnSpread
from deribit_arb_app.model.indicator_models.model_indicator_annualised_return_spread import \
                                                         ModelIndicatorAnnualisedReturnSpread

    #########################################################################################################
    # TestCase Testing funcitonality to calculate aned subscribe to internally calculated Annualised Spread #
    #########################################################################################################

class TestDeribitIndicatorAnnualizedReturnSpreadBuilderTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.currency = EnumCurrency.BTC.value
        self.instrument_kind = EnumInstrumentKind.FUTURE.value
        await TaskInstrumentsPull().run(currency=self.currency, kind=self.instrument_kind)
        self.store_instrument = Stores.store_subscribable_instruments
        self.instrument_1 = self.store_instrument.get_via_key('BTC-29SEP23')
        self.instrument_2 = self.store_instrument.get_via_key('BTC-29DEC23')
        
        self.index = ModelSubscribableIndex(name=EnumIndexCurrency.BTC.value)
        
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
        
        self.store_observable_indicator_annualized_return_spreads = Stores.store_indicator_annualised_return_spreads

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

    async def test_subscribe(self):
        await self.a_coroutine()