from deribit_arb_app.model.model_index import ModelIndex
from deribit_arb_app.model.model_instrument import ModelInstrument
from deribit_arb_app.model.indicator_models.model_indicator_annualised_return_spread import ModelIndicatorAnnualisedReturnSpread

from deribit_arb_app.services.service_api_deribit import ServiceApiDeribit
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.services.service_deribit_account_summary import ServiceDeribitAccountSummary
from deribit_arb_app.subjects.subject_indicator_annualised_return_spread import SubjectIndicatorAnnualisedReturnSpread
from deribit_arb_app.observers.observer_indicator_annualised_return_spread import ObserverIndicatorAnnualisedReturnSpread


class StrategyCashAndCarryBasic:

    def __init__(self, 
            instrument_1: ModelInstrument, 
            instrument_2: ModelInstrument, 
            index: ModelIndex) -> None:

        self.instrument_1 = instrument_1
        self.instrument_2 = instrument_2
        self.index = index

        # service dependencies
        self.api_deribit = ServiceApiDeribit()
        
        # initiate the relevant order book - get current market prices
        self.store_subject_order_books = StoreSubjectOrderBooks()

        # create and update the relevant indicator

        self.indicator_annualized_return_spread = ModelIndicatorAnnualisedReturnSpread(
                 instrument_1=instrument_1,
                 instrument_2=instrument_2,
                 index=index
        )

        # wrap the indicator in an observer that updates with every order_book, and index update
        
        self.observer_indicator_annualized_return_spread = \
            ObserverIndicatorAnnualisedReturnSpread(instance=self.indicator_annualized_return_spread)

    def run(self) -> None:
        
        # check the indicator value
        indicator_annualized_return_spread = self.observer_indicator_annualized_return_spread.get()

        if not indicator_annualized_return_spread:
                    return

        indicator_annualized_return_spread_value = indicator_annualized_return_spread.value

        if not indicator_annualized_return_spread_value:
            return

        indicator_annualized_return_spread_float = float(indicator_annualized_return_spread_value)

        if indicator_annualized_return_spread_float < 0.03:
            print('roll the spread')
        elif indicator_annualized_return_spread_float > 0.03:
            print('roll back the spread')
        else:
            print('No trade')
     
