import sys
import traceback

from singleton_decorator import singleton

from deribit_arb_app.observables.observable_indicator import ObservableIndicator
from deribit_arb_app.store.store_observable_interface import StoreObservableInterface
from deribit_arb_app.model.indicator_models.model_indicator_put_call_parity_arbitrage import ModelIndicatorPutCallVolArbitrage

    ######################################################################
    # Store Manages & Stores Put Call Parity Arbitrage Indicator objects #
    ######################################################################

@singleton
class StoreObservablePutCallParityArbitrage(StoreObservableInterface):

    def __init__(self):
        self.__observable_indicator_put_call_parity_arbitrages = {}

    def update_observable(self, indicator_put_call_parity_arbitrage: ModelIndicatorPutCallVolArbitrage):
        
        if indicator_put_call_parity_arbitrage is None:
            return

        if not indicator_put_call_parity_arbitrage.key in self.__observable_indicator_put_call_parity_arbitrages:
            self.__observable_indicator_put_call_parity_arbitrages[indicator_put_call_parity_arbitrage.key] = ObservableIndicator(indicator_put_call_parity_arbitrage)
        try:
            self.__observable_indicator_put_call_parity_arbitrages[indicator_put_call_parity_arbitrage.key].set_instance(indicator_put_call_parity_arbitrage)
            print(f"{indicator_put_call_parity_arbitrage.put_instrument.instrument_name}-{indicator_put_call_parity_arbitrage.call_instrument.instrument_name} Spread: {indicator_put_call_parity_arbitrage.value}")
        except Exception as e:
            print(e)
            _, _, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=None)

    def get_observable(self, indicator_put_call_parity_arbitrage: ModelIndicatorPutCallVolArbitrage):
        if not indicator_put_call_parity_arbitrage.key in self.__observable_indicator_put_call_parity_arbitrages:
            self.__observable_indicator_put_call_parity_arbitrages[indicator_put_call_parity_arbitrage.key] = ObservableIndicator(indicator_put_call_parity_arbitrage)
        return self.__observable_indicator_put_call_parity_arbitrages[indicator_put_call_parity_arbitrage.key]
    
    def remove_observable(self, indicator_put_call_parity_arbitrage: ModelIndicatorPutCallVolArbitrage):
        if indicator_put_call_parity_arbitrage is None:
            return

        if indicator_put_call_parity_arbitrage.key in self.__observable_indicator_put_call_parity_arbitrages:
            del self.__observable_indicator_put_call_parity_arbitrages[indicator_put_call_parity_arbitrage.key]