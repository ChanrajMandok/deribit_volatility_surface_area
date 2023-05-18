import sys
import traceback
from singleton_decorator import singleton

from deribit_arb_app.store.store_subjectable_interface import StoreSubjectableInterface
from deribit_arb_app.model.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread
from deribit_arb_app.subjects.subject_indicator_annualised_return_spread import SubjectIndicatorAnnualisedReturnSpread

    #####################################################################
    # Store Manages & Stores Annualized Return Spread Indicator objects #
    #####################################################################

@singleton
class StoreSubjectIndicatorAnnualizedReturnSpreads(StoreSubjectableInterface):

    def __init__(self):
        self.__subject_indicator_annualised_return_spreads = {}

    def update_subject(self, indicator_annualised_return_spread: ModelIndicatorAnnualisedReturnSpread):
        
        if indicator_annualised_return_spread is None:
            return

        if not indicator_annualised_return_spread.key in self.__subject_indicator_annualised_return_spreads:
            self.__subject_indicator_annualised_return_spreads[indicator_annualised_return_spread.key] = SubjectIndicatorAnnualisedReturnSpread(indicator_annualised_return_spread)
        try:
            self.__subject_indicator_annualised_return_spreads[indicator_annualised_return_spread.key].set_instance(indicator_annualised_return_spread)
            print(f"{indicator_annualised_return_spread.instrument_1.instrument_name}-{indicator_annualised_return_spread.instrument_2.instrument_name} Spread: {indicator_annualised_return_spread.value}")
        except Exception as e:
            print(e)
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)

    def get_subject(self, indicator_annualised_return_spread: ModelIndicatorAnnualisedReturnSpread) -> SubjectIndicatorAnnualisedReturnSpread:
        if not indicator_annualised_return_spread.key in self.__subject_indicator_annualised_return_spreads:
            self.__subject_indicator_annualised_return_spreads[indicator_annualised_return_spread.key] = SubjectIndicatorAnnualisedReturnSpread(indicator_annualised_return_spread)
        return self.__subject_indicator_annualised_return_spreads[indicator_annualised_return_spread.key]
    
    def remove_subject(self, indicator_annualised_return_spread: ModelIndicatorAnnualisedReturnSpread):
        if indicator_annualised_return_spread is None:
            return

        if indicator_annualised_return_spread.key in self.__subject_indicator_annualised_return_spreads:
            del self.__subject_indicator_annualised_return_spreads[indicator_annualised_return_spread.key]