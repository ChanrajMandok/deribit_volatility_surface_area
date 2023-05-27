from singleton_decorator import singleton

from deribit_arb_app.observers.observer_interface import ObserverInterface
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.store.store_subject_indicator_annualized_return_spreads import StoreSubjectIndicatorAnnualizedReturnSpreads
from deribit_arb_app.model.indicator_models.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread
from deribit_arb_app.services.builders.service_indicator_annualised_return_spread_builder import ServiceIndicatorAnnualisedReturnSpreadBuilder

    #########################################################################
    # Observer monitors the Annualised Return Spead between two instruments #
    #########################################################################
    
@singleton
class ObserverIndicatorAnnualisedReturnSpread(ObserverInterface):

    def __init__(self) -> None:
        super().__init__()
        self.indicators = {}
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.store_subject_index_prices = StoreSubjectIndexPrices()
        self.service_builder = ServiceIndicatorAnnualisedReturnSpreadBuilder()
        self.store_subject_indicator_annualized_return_spreads = StoreSubjectIndicatorAnnualizedReturnSpreads()

    def attach_indicator(self, instance: ModelIndicatorAnnualisedReturnSpread):
        key = instance.key
        self.indicators[key] = instance

        # Attach this observer to the relevant subjects: the order book and the index price
        for instrument in [instance.instrument_1, instance.instrument_2]:
            self.store_subject_order_books.get_subject(instrument).attach(self)
        self.store_subject_index_prices.get_subject(instance.index).attach(self)

    def update(self):
        for key, instance in self.indicators.items():
            try:
                indicator = self.service_builder.build(instance)
                if indicator is not None:
                    self.store_subject_indicator_annualized_return_spreads.update_subject(indicator)
            except Exception as e:
                print(f"Error updating indicator: {instance.key}")
                print(f"Error message: {str(e)}")

    def get(self, key) -> ModelIndicatorAnnualisedReturnSpread:
        return self.indicators.get(key)

    def detach_indicator(self, key):
        instance = self.indicators[key]
        for instrument in [instance.instrument_1, instance.instrument_2]:
            self.store_subject_order_books.get_subject(instrument).detach(self)
        self.store_subject_index_prices.get_subject(instance.index).detach(self)

    def detach_all(self):
        for key in list(self.indicators.keys()):
            self.detach_indicator(key)
