from typing import List
from singleton_decorator import singleton
from concurrent.futures import ThreadPoolExecutor

from deribit_arb_app.observers.observer_interface import ObserverInterface
from deribit_arb_app.store.store_subject_order_books import StoreSubjectOrderBooks
from deribit_arb_app.store.store_subject_index_prices import StoreSubjectIndexPrices
from deribit_arb_app.services.builders.service_implied_volatilty_bsm_builder import ServiceImpliedVolatilityBsmBuilder
from deribit_arb_app.store.store_subject_indicator_bsm_implied_volatilty import StoreSubjectIndicatorBsmImpliedVolatilty
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility

    ###################################################################################################
    # Observer monitors the instrument orderbook & index price feed and updates BSM Implied volatilty #
    ###################################################################################################

@singleton
class ObserverIndicatorBsmImpliedVolatility(ObserverInterface):

    def __init__(self) -> None:
        super().__init__()
        self.indicators = {}
        self.store_subject_order_books = StoreSubjectOrderBooks()
        self.store_subject_index_prices = StoreSubjectIndexPrices()
        self.store_subject_indicator_bsm_iv = StoreSubjectIndicatorBsmImpliedVolatilty()
        self.service_implied_volatilty_bsm_builder = ServiceImpliedVolatilityBsmBuilder()

    def attach_indicator(self, instance: ModelIndicatorBsmImpliedVolatility):
        key = instance.key
        instrument = instance.instrument
        index = instance.index
        self.indicators[key] = instance

        # Attach observer to instrument order book and index
        self.store_subject_order_books.get_subject(instrument).attach(self)
        self.store_subject_index_prices.get_subject(index).attach(self)

    def detach_indicator(self, key):
        instance = self.indicators.get(key)
        if instance:
            instrument = instance.instrument
            index = instance.index

            # Detach observer from instrument order book and index
            self.store_subject_order_books.get_subject(instrument).detach(self)
            self.store_subject_index_prices.get_subject(index).detach(self)

            del self.indicators[key]

    def update(self) -> None:
        with ThreadPoolExecutor(max_workers=4) as executor:
            tasks = [(key, executor.submit(self.service_implied_volatilty_bsm_builder.build, indicator))
                    for key, indicator in self.indicators.items()]

            for key, future in tasks:
                try:
                    result = future.result()
                    if result is not None:
                        self.store_subject_indicator_bsm_iv.update_subject(key, result)
                except Exception as e:
                    print(f"Error updating indicator: {key}")
                    print(f"Error message: {str(e)}")

    def get(self) -> List[ModelIndicatorBsmImpliedVolatility]:
        return list(self.indicators.values())

    def detach_all(self):
        for key in list(self.indicators.keys()):
            self.detach_indicator(key)

    ## cannot update many as bsm must be ran every single time