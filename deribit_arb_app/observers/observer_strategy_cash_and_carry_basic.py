from deribit_arb_app.observers.observer_interface import ObserverInterface
from deribit_arb_app.strategies.strategy_cash_and_carry_basic import StrategyCashAndCarryBasic
from deribit_arb_app.store.store_subject_indicator_annualized_return_spreads import StoreSubjectIndicatorAnnualizedReturnSpreads

    ############################################################################
    # Observer monitors Cash & Carry Strategy (Spread between Future and Spot) #
    ############################################################################

class ObserverStrategyCashAndCarryBasic(ObserverInterface):
    
    # holds the subject-observer logic
    # attach and detach the observer from the subject's observers list

    def __init__(self, instance: StrategyCashAndCarryBasic) -> None:

        super().__init__()

        self.__strategy_cash_and_carry_basic= instance
        
        self.indicator_annualized_return_spread = instance.indicator_annualized_return_spread

        self.store_subject_indicator_annualized_return_spreads = StoreSubjectIndicatorAnnualizedReturnSpreads()

        # attach this observer to the relevant subjects: the order book and the index price
        self.store_subject_indicator_annualized_return_spreads.get_subject(self.indicator_annualized_return_spread).attach(self)

    def update(self):
        if self.__strategy_cash_and_carry_basic is None:
            return
        print("run strategy...")
        self.__strategy_cash_and_carry_basic.run()

    def get(self) -> StrategyCashAndCarryBasic:
        return self.__strategy_cash_and_carry_basic

    def __exit__(self):
        self.store_subject_indicator_annualized_return_spreads.get_subject(self.indicator_annualized_return_spread).detach(self)