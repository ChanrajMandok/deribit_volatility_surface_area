import os
import asyncio
import traceback

from typing import Optional
from singleton_decorator import singleton

from deribit_arb_app.observers import logger
from deribit_arb_app.store.stores import Stores
from deribit_arb_app.model.model_observable_order_book import \
                                       ModelObservableOrderBook
from deribit_arb_app.model.model_observable_index_price import \
                                       ModelObservableIndexPrice
from deribit_arb_app.model.model_observable import ModelObservable
from deribit_arb_app.model.model_observable_volatility_index import \
                                       ModelObservableVolatilityIndex
from deribit_arb_app.observers.observer_interface import ObserverInterface
from deribit_arb_app.services.builders.service_implied_volatility_bsm_builder import \
                                                    ServiceImpliedVolatilityBsmBuilder
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import \
                                                         ModelIndicatorBsmImpliedVolatility
                                                         
    ####################################################################################################
    # Observer monitors the instrument orderbook & index price feed and updates BSM Implied volatility #
    ####################################################################################################

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
        self.index_price_exists = False
        self.implied_volatility_dict = {}  # Stores the latest implied volatilities
        self.volatility_index_exists = False
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


    def update(self, 
               observable: ModelObservable):
        """
        Main update method called when observed subjects change.
        Delegates to specific update methods based on the type of observable.

        Args:
            observable: The observable object that triggered the update.
        """
        try:
            if isinstance(observable, ModelObservableOrderBook):
                self.update_order_book(observable)
            
            # Update based on observable type
            elif isinstance(observable, ModelObservableVolatilityIndex):
                self.update_volatility_index()

            elif isinstance(observable, ModelObservableIndexPrice):
                self.update_index_price()

        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                    f"Stack trace: {traceback.format_exc()}")


    def update_volatility_index(self):
        """
        Update all indicators based on changes in the volatility index.
        """
        for _, indicator in self.indicators.items():
            self.update_indicator(indicator)


    def update_index_price(self):
        """
        Update all indicators based on changes in the index price.
        """
        
        for _, indicator in self.indicators.items():
            self.update_indicator(indicator)


    def update_order_book(self, observable):
        """
        Update a specific indicator based on changes in the orderbook.

        Args:
            observable: The observable order book that triggered the update.
        """
        # Generate key from observable name
        indicator_key = ModelIndicatorBsmImpliedVolatility().\
                        generate_key_from_str(instrument=observable.name)
        indicator = self.indicators.get(indicator_key)

        if indicator is None:
            ValueError(f'key {observable.name} not in indicators')
            return
            
        self.update_indicator(indicator)

    def update_indicator(self, 
                         indicator: ModelIndicatorBsmImpliedVolatility):
        """
        Perform the update operation for a given indicator.

        Args:
            indicator: The indicator to be updated.
        """
        # Build result and populate the queue if valid
        result = self.service_implied_volatility_bsm_builder.build(indicator)
        if result:
            result.time_to_maturity = round(result.time_to_maturity, 4)
            result.implied_volatility = round(result.implied_volatility, 4)
            self.populate_implied_volatility_queue(result=result)


    def detach_all(self):
        """
        Detaches all indicators from this observer.
        """
        for key in list(self.indicators.keys()):
            self.detach_indicator(key)


    def populate_implied_volatility_queue(self, 
                                          result: ModelIndicatorBsmImpliedVolatility):
        """
        Populates the implied volatility queue with the result if there is a change.
        """
        try:
            existing_iv = self.implied_volatility_dict.get(result.name)
            # Update if there's a change in implied volatility
            if existing_iv is None or existing_iv != result.implied_volatility:
                self.implied_volatility_dict[result.name] = result.implied_volatility
                self.implied_volatility_queue.put_nowait(result)
                # print(f"{result.name, result.implied_volatility}")
        
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                    f"Stack trace: {traceback.format_exc()}")