import sys
import traceback

from singleton_decorator import singleton

from deribit_arb_app.observables.observable_indicator import ObservableIndicator
from deribit_arb_app.store.store_observable_interface import StoreObservableInterface
from deribit_arb_app.model.indicator_models.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread

    #####################################################################
    # Store Manages & Stores Annualized Return Spread Indicator objects #
    #####################################################################

@singleton
class StoreObservableIndicatorAnnualizedReturnSpreads(StoreObservableInterface):
    
    def __init__(self):
        self.__observable_indicator_annualised_return_spreads = {}

    def update_observable(self, indicator_annualised_return_spread: ModelIndicatorAnnualisedReturnSpread):
        
        if indicator_annualised_return_spread is None:
            return

        if not indicator_annualised_return_spread.key in self.__observable_indicator_annualised_return_spreads:
            self.__observable_indicator_annualised_return_spreads[indicator_annualised_return_spread.key] = ObservableIndicator(indicator_annualised_return_spread)
        try:
            self.__observable_indicator_annualised_return_spreads[indicator_annualised_return_spread.key].set_instance(indicator_annualised_return_spread)
            print(f"{indicator_annualised_return_spread.instrument_1.instrument_name}-{indicator_annualised_return_spread.instrument_2.instrument_name} Spread: {indicator_annualised_return_spread.value}")
        except Exception as e:
            print(e)
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)

    def get_observable(self, indicator_annualised_return_spread: ModelIndicatorAnnualisedReturnSpread):
        if not indicator_annualised_return_spread.key in self.__observable_indicator_annualised_return_spreads:
            self.__observable_indicator_annualised_return_spreads[indicator_annualised_return_spread.key] = ObservableIndicator(indicator_annualised_return_spread)
        return self.__observable_indicator_annualised_return_spreads[indicator_annualised_return_spread.key]
    
    def remove_observable(self, indicator_annualised_return_spread: ModelIndicatorAnnualisedReturnSpread):
        if indicator_annualised_return_spread is None:
            return

        if indicator_annualised_return_spread.key in self.__observable_indicator_annualised_return_spreads:
            del self.__observable_indicator_annualised_return_spreads[indicator_annualised_return_spread.key]