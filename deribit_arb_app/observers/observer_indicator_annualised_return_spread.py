from singleton_decorator import singleton

from deribit_arb_app.store.stores import Stores
from deribit_arb_app.observers.observer_interface import ObserverInterface
from deribit_arb_app.model.indicator_models.model_indicator_annualised_return_spread import \
                                                        ModelIndicatorAnnualisedReturnSpread
from deribit_arb_app.services.builders.service_indicator_annualised_return_spread_builder import \
                                                    ServiceIndicatorAnnualisedReturnSpreadBuilder

    #########################################################################
    # Observer monitors the Annualised Return Spead between two instruments #
    #########################################################################
    
@singleton
class ObserverIndicatorAnnualisedReturnSpread(ObserverInterface):

    def __init__(self) -> None:
        super().__init__()
        self.indicators = {}
        self.store_observable_order_books = Stores.store_observable_orderbooks
        self.store_observable_index_prices = Stores.store_observable_index_prices
        self.service_builder = ServiceIndicatorAnnualisedReturnSpreadBuilder()
        self.store_observable_indicator_annualised_spread = Stores.store_indicator_annualised_return_spreads

    def attach_indicator(self, instance: ModelIndicatorAnnualisedReturnSpread):
        """ Attach this observer to the instance """
        key = instance.key
        self.indicators[key] = instance

        # Attach this observer to the relevant observable: the order book and the index price
        for instrument in [instance.instrument_1, instance.instrument_2]:
            self.store_observable_order_books.get_observable(instrument).attach(self)
        self.store_observable_index_prices.get_observable(instance.index).attach(self)

    def update(self):
        for key, instance in self.indicators.items():
            try:
                indicator = self.service_builder.build(instance)
                if indicator is not None:
                    self.store_observable_indicator_annualised_spread.update_observable(indicator)
            except Exception as e:
                raise Exception(f"{self.__class__.__name__}: {e}")

    def get(self, key) -> ModelIndicatorAnnualisedReturnSpread:
        return self.indicators.get(key)

    def detach_indicator(self, key):
        """ Detach this observer from the instance """
        instance = self.indicators[key]
        for instrument in [instance.instrument_1, instance.instrument_2]:
            self.store_observable_order_books.get_observable(instrument).detach(self)
        self.store_observable_index_prices.get_observable(instance.index).detach(self)

    def detach_all(self):
        for key in list(self.indicators.keys()):
            self.detach_indicator(key)
