import os
import numpy as np

from collections import defaultdict
from datetime import datetime, timedelta
from singleton_decorator import singleton
from scipy.interpolate import griddata, RectBivariateSpline

from deribit_arb_app.services import logger
from deribit_arb_app.services.plot.service_plot_volatility_surface_area import \
                                                ServicePlotVolatilitySurfaceArea
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import \
                                                         ModelIndicatorBsmImpliedVolatility

    ##################################################
    # Service Manages Volatility Surface Area Object #
    ##################################################

@singleton
class ServiceImpliedVolatiltySurfaceAreaObjectManager():

    def __init__(self) -> None:
        # Initializing arrays and flags for the volatility surface
        self.iv_array = None
        self.ttm_array = None
        self.create_plot = False
        self.moneyness_array = None
        
        # Initializing data structures for keeping track of volatilities and their counts
        self.counts = defaultdict(int)
        self.vol_dict = defaultdict(lambda: (0.0, datetime.min))
        
        # Service for plotting volatility surface
        self.service_plot_volatility_surface_area = ServicePlotVolatilitySurfaceArea()
        self.max_vsa_object_life_seconds = int(os.environ.get('MAX_VSA_OBJECT_LIFE_SECONDS', 300))

    def create_vsa_surface(self, plot: bool,
                           model_iv_objects: list[ModelIndicatorBsmImpliedVolatility]) -> np.ndarray:
        # Create the initial volatility surface array
        if plot:
            self.create_plot = True
        try:
            self._update_vol_dict_and_counts(model_iv_objects)
            self._update_surface()
            logger.info(f"{self.__class__.__name__}: VSA Object created")
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error in create_vsa_surface: {e}")

    def update_vsa_surface(self, model_iv_objects: list[ModelIndicatorBsmImpliedVolatility]) -> np.ndarray:
        # Update the volatility surface array with new data
        try:
            self._update_vol_dict_and_counts(model_iv_objects)
            self._remove_stale_entries()
            self._update_surface()
            logger.info(f"{self.__class__.__name__}: VSA Object updated")
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error in update_vsa_surface: {e}")

    def _update_vol_dict_and_counts(self, model_iv_objects: list[ModelIndicatorBsmImpliedVolatility]) -> None:
        # Update volatilities in the dictionary with new data
        try:
            for model_iv_object in model_iv_objects:
                reciprocal_spot = 1.0 / model_iv_object.spot
                moneyness = round(model_iv_object.strike * reciprocal_spot, 5)
                dte = int(round(model_iv_object.time_to_maturity * 365))
                key = (moneyness, dte)
                current_time = datetime.now()
                old_vol, old_time = self.vol_dict[key]
                # Incremental average calculation for implied volatility
                updated_vol = (old_vol * self.counts[key] + model_iv_object.implied_volatility) / \
                    (self.counts[key] + 1) if old_time > current_time - timedelta(
                    seconds=self.max_vsa_object_life_seconds) else model_iv_object.implied_volatility
                self.vol_dict[key] = (updated_vol, current_time)
                self.counts[key] = self.counts[key] + 1 if old_time > current_time - timedelta(
                    seconds=self.max_vsa_object_life_seconds) else 1
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error in update_vol_dict_and_counts: {e}")

    def _remove_stale_entries(self) -> None:
        # Remove entries that are older than a defined threshold
        try:
            current_time = datetime.now()
            to_remove = [key for key, (vol, timestamp) in self.vol_dict.items() if
                         timestamp <= current_time - timedelta(seconds=self.max_vsa_object_life_seconds)]
            for key in to_remove:
                del self.vol_dict[key]
                del self.counts[key]
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error in remove_stale_entries: {e}")

    def _update_surface(self) -> None:
        try:
            all_moneyness, all_maturities, all_vols = zip(*[(moneyness, dte, vol) for (moneyness, dte), (vol, timestamp) in self.vol_dict.items()])
            moneyness_values = np.linspace(min(all_moneyness), max(all_moneyness), 200)
            days_to_expiry = np.linspace(min(all_maturities), max(all_maturities), 200)
            self.moneyness_array, self.ttm_array = np.meshgrid(moneyness_values, days_to_expiry)
            self.iv_array = griddata((all_moneyness, all_maturities), all_vols, (self.moneyness_array, self.ttm_array), method='linear') 
            self.arbitrage_free_adjustment()

            if self.create_plot:
                if self.service_plot_volatility_surface_area.surface:
                    self.service_plot_volatility_surface_area.update_plot(iv_array=self.iv_array,
                                                                        ttm_array=self.ttm_array,
                                                                        moneyness_array=self.moneyness_array)
                    self.service_plot_volatility_surface_area.show()
                else:
                    self.service_plot_volatility_surface_area.create_plot(iv_array=self.iv_array,
                                                                        ttm_array=self.ttm_array,
                                                                        moneyness_array=self.moneyness_array)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error in _update_surface: {e}")

    def arbitrage_free_adjustment(self):
        """
        Adjust the volatility surface to make it arbitrage-free using RectBivariateSpline.
        """

        # Extract the unique maturities and moneyness to create a grid for splines.
        unique_maturities = np.unique(self.ttm_array)
        unique_moneyness = np.unique(self.moneyness_array)
        
        # Use RectBivariateSpline to fit the data. This creates a smooth surface.
        spline = RectBivariateSpline(unique_maturities, unique_moneyness, self.iv_array)

        # Re-evaluate the implied volatilities using the spline directly into self.iv_array
        np.maximum(spline.ev(self.ttm_array, self.moneyness_array), self.iv_array, out=self.iv_array)
        
        # Apply the monotonicity conditions to ensure arbitrage-freeness.

        # 1. Monotonicity in Time-to-Maturity (Calendar Arbitrage)
        np.maximum.accumulate(self.iv_array, axis=0, out=self.iv_array)

        # 2. Monotonicity in Strikes (Strike Arbitrage)
        np.minimum.accumulate(self.iv_array[:, ::-1], axis=1, out=self.iv_array[:, ::-1])
        
        # 3. Monotonicity in the second derivative of Strikes (Butterfly Arbitrage)
        for i in range(1, self.moneyness_array.shape[1] - 1):
            np.maximum(2 * self.iv_array[:, i] - np.maximum(self.iv_array[:, i - 1], self.iv_array[:, i + 1]), 
                    self.iv_array[:, i], out=self.iv_array[:, i])