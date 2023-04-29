from singleton_decorator import singleton
from deribit_arb_app.observers.observer_interface import ObserverInterface
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.model.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread
from deribit_arb_app.store.store_subject_indicator_annualized_return_spreads import StoreSubjectIndicatorAnnualizedReturnSpreads
from deribit_arb_app.services.service_indicator_annualised_return_spread_builder import ServiceIndicatorAnnualisedReturnSpreadBuilder

    #########################################################################
    # Observer monitors the Annualised Return Spead between two instruments #
    #########################################################################
    
@singleton
class ObserverIndicatorAnnualisedReturnSpread(ObserverInterface):

    # holds the subject-observer logic
    # attach and detach the observer from the subject's observers list

    def __init__(self, instance: ModelIndicatorAnnualisedReturnSpread) -> None:
        super().__init__()
        self.__indicator_annualised_return_spread = None
        self.instrument_1 = instance.instrument_1
        self.instrument_2 = instance.instrument_2
        self.index = instance.index
        
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.store_subject_index_prices = StoreSubjectIndexPrices()
        self.store_subject_indicator_annualized_return_spreads = StoreSubjectIndicatorAnnualizedReturnSpreads()

        self.service_indicator_annualised_return_spread_builder = ServiceIndicatorAnnualisedReturnSpreadBuilder(instance)
        
        # attach this observer to the relevant subjects: the order book and the index price

        for instrument in [self.instrument_1, self.instrument_2]:
            self.store_subject_order_books.get_subject(instrument).attach(self)
        self.store_subject_index_prices.get_subject(self.index).attach(self)
        

    def update(self):
        self.__indicator_annualised_return_spread = self.service_indicator_annualised_return_spread_builder.build()
        if self.__indicator_annualised_return_spread is None:
            return
        print(f"{self.__indicator_annualised_return_spread.key}: {round(self.__indicator_annualised_return_spread.value,6)}%")
        self.store_subject_indicator_annualized_return_spreads.update_subject(self.__indicator_annualised_return_spread)

    def get(self) -> ModelIndicatorAnnualisedReturnSpread:
        return self.__indicator_annualised_return_spread

    def __exit__(self):
        for instrument in [self.instrument_1, self.instrument_2]:
            self.store_subject_order_books.get_subject(instrument).detach(self)   
        self.store_subject_index_prices.get_subject(self.index).detach(self)
