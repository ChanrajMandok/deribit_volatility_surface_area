from typing import List
from singleton_decorator import singleton
from concurrent.futures import ThreadPoolExecutor

from deribit_arb_app.observers.observer_interface import ObserverInterface
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.model.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility
from deribit_arb_app.services.builders.service_implied_volatilty_bsm_builder import ServiceImpliedVolatilityBsmBuilder
from deribit_arb_app.store.store_subject_indicator_bsm_implied_volatilty import StoreSubjectIndicatorBsmImpliedVolatilty

    ###################################################################################################
    # Observer monitors the instrument orderbook & index price feed and updates BSM Implied volatilty #
    ###################################################################################################

@singleton
class ObserverIndicatorBsmImpliedVolatility(ObserverInterface):

    def __init__(self, instances:List[ModelIndicatorBsmImpliedVolatility]) -> None:
        super().__init__()
        self.indicators = {}
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.store_subject_index_prices = StoreSubjectIndexPrices()
        self.store_subject_indicator_bsm_iv = StoreSubjectIndicatorBsmImpliedVolatilty()
        
        for instance in instances:
            key = instance.key
            instrument = instance.instrument
            index = instance.index
            self.indicators[key] = instance

            # Attach observer to instrument orderbook and index
            self.store_subject_order_books.get_subject(instrument).attach(self)
            self.store_subject_index_prices.get_subject(index).attach(self)

    def update(self) -> None:

        ## build has computationally intense BSM calculation so threading is utilised
        with ThreadPoolExecutor(max_workers=4) as executor:
            tasks = []
            for key, indicator in self.indicators.items():
                service_implied_volatilty_bsm_builder = ServiceImpliedVolatilityBsmBuilder(indicator)
                task = executor.submit(service_implied_volatilty_bsm_builder.build)
                tasks.append((key, task))
            
            for key, task in tasks:
                result = task.result()
                if result is None:
                    continue
                print(f"{result.key}: {round(result.value, 6)}")
                self.store_subject_indicator_bsm_iv.update_subject(key, result)

    def get(self) -> List[ModelIndicatorBsmImpliedVolatility]:
        return list(self.indicators.values())

    def __exit__(self):
        for key, indicator in self.indicators.items():
            instrument = indicator.instrument
            index = indicator.index
            self.store_subject_order_books.get_subject(instrument).detach(self)
            self.store_subject_index_prices.get_subject(index).detach(self)