import os
import asyncio
import traceback

from singleton_decorator import singleton

from deribit_arb_app.observers import logger
from deribit_arb_app.store.stores import Stores
from deribit_arb_app.observers.observer_interface import ObserverInterface
from deribit_arb_app.services.builders.service_implied_volatility_bsm_builder import \
                                                    ServiceImpliedVolatilityBsmBuilder
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import \
                                                         ModelIndicatorBsmImpliedVolatility

    ###################################################################################################
    # Observer monitors the instrument orderbook & index price feed and updates BSM Implied volatility #
    ###################################################################################################

@singleton
class ObserverIndicatorBsmImpliedVolatility(ObserverInterface):
    """
    Observer class for tracking and updating BSM (Black-Scholes-Merton) Implied Volatility indicators.
    Implements Observer pattern to respond to changes in market data.
    """

    def __init__(self,
                 implied_volatility_queue: asyncio.Queue) -> None:
        super().__init__()
        self.indicators = {}  # Stores the attached indicators
        self.implied_volatility_dict = {}  # Stores the latest implied volatilities
        self.max_workers = os.environ.get('MAX_WORKERS', 6)  # Number of workers for parallel processing
        self.implied_volatility_queue = implied_volatility_queue  # Queue for implied volatility results
        # References to observable stores for order books, index prices, and volatility indices
        self.store_observable_order_books = Stores.store_observable_orderbooks
        self.store_observable_index_prices = Stores.store_observable_index_prices
        self.store_observable_volatility_index = Stores.store_observable_volatility_index
        self.service_implied_volatility_bsm_builder = ServiceImpliedVolatilityBsmBuilder()


    def attach_indicator(self,
                         instance: ModelIndicatorBsmImpliedVolatility):
        """
        Attaches an implied volatility indicator instance to this observer.

        Args:
            instance (ModelIndicatorBsmImpliedVolatility): The indicator instance to attach.
        """
        
        key = instance.key  # Unique key for the indicator
        # Attach this observer to the relevant order books and indices
        self.indicators[key] = instance
        self.store_observable_order_books.get_observable(instance.instrument).attach(self)
        self.store_observable_index_prices.get_observable(instance.index).attach(self)
        self.store_observable_volatility_index.get_observable(instance.volatility_index).attach(self)


    def detach_indicator(self, key):
        """
        Detaches an implied volatility indicator instance from this observer.
        """
        instance = self.indicators.get(key)
        if instance:
            # Detach this observer from the relevant order books and indices
            self.store_observable_order_books.get_observable(instance.instrument).detach(self)
            self.store_observable_index_prices.get_observable(instance.index).detach(self)
            self.store_observable_volatility_index.get_observable(instance.volatility_index).detach(self)
            del self.indicators[key]  # Remove the indicator from tracking


    def update(self):
        """
        Update method called when observed subjects change. It recalculates the implied volatilities.
        """
        for key, indicator in self.indicators.items():
            try:
                result = self.service_implied_volatility_bsm_builder.build(indicator)
                if result:
                    # Round the time to maturity and implied volatility for precision
                    result.time_to_maturity = round(result.time_to_maturity, 4)
                    result.implied_volatility = round(result.implied_volatility, 4)

                    existing_iv = self.implied_volatility_dict.get(result.name)
                    # Update the implied volatility dictionary and queue if there's a change
                    if existing_iv is None or existing_iv != result.implied_volatility:
                        self.implied_volatility_dict[result.name] = result.implied_volatility
                        self.implied_volatility_queue.put_nowait(result)
                        print(f"{self.implied_volatility_dict[result.name], result.implied_volatility}")
            except Exception as e:
                logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                        f"Stack trace: {traceback.format_exc()}")


    def detach_all(self):
        """
        Detaches all indicators from this observer.
        """
        for key in list(self.indicators.keys()):
            self.detach_indicator(key)