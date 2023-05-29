import sys
import traceback

from singleton_decorator import singleton

from deribit_arb_app.subjects.subject_indicator import SubjectIndicator
from deribit_arb_app.store.store_subjectable_interface import StoreSubjectableInterface
from deribit_arb_app.model.indicator_models.model_indicator_put_call_parity_arbitrage import ModelIndicatorPutCallParityArbitrage

    ######################################################################
    # Store Manages & Stores Put Call Parity Arbitrage Indicator objects #
    ######################################################################

@singleton
class StoreSubjectPutCallParityArbitrage(StoreSubjectableInterface):

    def __init__(self):
        self.__subject_indicator_put_call_parity_arbitrages = {}

    def update_subject(self, indicator_put_call_parity_arbitrage: ModelIndicatorPutCallParityArbitrage):
        
        if indicator_put_call_parity_arbitrage is None:
            return

        if not indicator_put_call_parity_arbitrage.key in self.__subject_indicator_put_call_parity_arbitrages:
            self.__subject_indicator_put_call_parity_arbitrages[indicator_put_call_parity_arbitrage.key] = SubjectIndicator(indicator_put_call_parity_arbitrage)
        try:
            self.__subject_indicator_put_call_parity_arbitrages[indicator_put_call_parity_arbitrage.key].set_instance(indicator_put_call_parity_arbitrage)
            print(f"{indicator_put_call_parity_arbitrage.put_instrument.instrument_name}-{indicator_put_call_parity_arbitrage.call_instrument.instrument_name} Spread: {indicator_put_call_parity_arbitrage.value}")
        except Exception as e:
            print(e)
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)

    def get_subject(self, indicator_put_call_parity_arbitrage: ModelIndicatorPutCallParityArbitrage):
        if not indicator_put_call_parity_arbitrage.key in self.__subject_indicator_put_call_parity_arbitrages:
            self.__subject_indicator_put_call_parity_arbitrages[indicator_put_call_parity_arbitrage.key] = SubjectIndicator(indicator_put_call_parity_arbitrage)
        return self.__subject_indicator_put_call_parity_arbitrages[indicator_put_call_parity_arbitrage.key]
    
    def remove_subject(self, indicator_put_call_parity_arbitrage: ModelIndicatorPutCallParityArbitrage):
        if indicator_put_call_parity_arbitrage is None:
            return

        if indicator_put_call_parity_arbitrage.key in self.__subject_indicator_put_call_parity_arbitrages:
            del self.__subject_indicator_put_call_parity_arbitrages[indicator_put_call_parity_arbitrage.key]