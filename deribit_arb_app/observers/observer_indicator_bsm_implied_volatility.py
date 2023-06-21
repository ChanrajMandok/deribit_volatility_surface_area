import os
import asyncio
from singleton_decorator import singleton
from concurrent.futures import ThreadPoolExecutor

from deribit_arb_app.observers.observer_interface import ObserverInterface
from deribit_arb_app.store.store_observable_order_books import StoreObservableOrderBooks
from deribit_arb_app.store.store_observable_index_prices import StoreObservableIndexPrices
from deribit_arb_app.services.builders.service_implied_volatility_bsm_builder import ServiceImpliedVolatilityBsmBuilder
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import ModelIndicatorBsmImpliedVolatility

    ###################################################################################################
    # Observer monitors the instrument orderbook & index price feed and updates BSM Implied volatility #
    ###################################################################################################

@singleton
class ObserverIndicatorBsmImpliedVolatility(ObserverInterface):

    def __init__(self, implied_volatility_queue:asyncio.Queue) -> None:
        super().__init__()
        self.indicators = {}
        self.implied_volatility_dict = {}
        self.max_workers = os.environ.get('MAX_WORKERS', None)
        self.implied_volatility_queue = implied_volatility_queue
        self.store_observable_order_books = StoreObservableOrderBooks()
        self.store_observable_index_prices = StoreObservableIndexPrices()
        self.service_implied_volatility_bsm_builder = ServiceImpliedVolatilityBsmBuilder()

    def attach_indicator(self, instance: ModelIndicatorBsmImpliedVolatility):
        key = instance.key
        instrument = instance.instrument
        index = instance.index
        self.indicators[key] = instance

        # Attach observer to instrument order book and index
        self.store_observable_order_books.get_observable(instrument).attach(self)
        self.store_observable_index_prices.get_observable(index).attach(self)

    def detach_indicator(self, key):
        instance = self.indicators.get(key)
        if instance:
            instrument = instance.instrument
            index = instance.index

            # Detach observer from instrument order book and index
            self.store_observable_order_books.get_observable(instrument).detach(self)
            self.store_observable_index_prices.get_observable(index).detach(self)

            del self.indicators[key]

    def update(self) -> None:
        with ThreadPoolExecutor(int(self.max_workers)) as executor:
            tasks = [(key, executor.submit(self.service_implied_volatility_bsm_builder.build, indicator))
                    for key, indicator in self.indicators.items()]

            for key, future in tasks:
                try:
                    result = future.result()
                    if result is not None:
                        if result is not None:
                            if result.name not in self.implied_volatility_dict or \
                                    round(self.implied_volatility_dict[result.name].implied_volatility, 4) != round(result.implied_volatility, 4):
                                self.implied_volatility_queue.put_nowait(result)
                except Exception as e:
                    print(f"Error updating indicator: {key}")
                    print(f"Error message: {str(e)}")

    def detach_all(self):
        for key in list(self.indicators.keys()):
            self.detach_indicator(key)