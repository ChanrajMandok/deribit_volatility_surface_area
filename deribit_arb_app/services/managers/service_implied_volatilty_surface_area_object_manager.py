import os
import numpy as np

from collections import defaultdict
from scipy.interpolate import griddata
from datetime import datetime, timedelta
from singleton_decorator import singleton

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
        self.iv_array = None
        self.ttm_array = None
        self.create_plot = False
        self.moneyness_array = None
        self.counts = defaultdict(int)
        self.vol_dict = defaultdict(lambda: (0.0, datetime.min))
        self.service_plot_volatility_surface_area = ServicePlotVolatilitySurfaceArea()
        self.max_vsa_object_life_seconds = int( os.environ.get('MAX_VSA_OBJECT_LIFE_SECONDS', 300))
        
    def create_vsa_surface(self, 
                           plot: bool,
                           model_iv_objects: list[ModelIndicatorBsmImpliedVolatility]) -> np.ndarray:
        
        if plot:
            self.create_plot = True
        try:
            self._update_vol_dict_and_counts(model_iv_objects)
            self._update_surface()
            logger.info(f"{self.__class__.__name__}: VSA Object created")
        
        except Exception as e:
                logger.error(f"{self.__class__.__name__}: Error in create_vsa_surface: {e}")

    def update_vsa_surface(self, model_iv_objects: list[ModelIndicatorBsmImpliedVolatility]) -> np.ndarray:
        try:
            self._update_vol_dict_and_counts(model_iv_objects)
            self._remove_stale_entries()
            self._update_surface()
            logger.info(f"{self.__class__.__name__}: VSA Object updated")
        
        except Exception as e:
                logger.error(f"{self.__class__.__name__}: Error in update_vsa_surface: {e}")

    def _update_vol_dict_and_counts(self, model_iv_objects: list[ModelIndicatorBsmImpliedVolatility]) -> None:
        try:
            for model_iv_object in model_iv_objects:
                reciprocal_spot = 1.0 / model_iv_object.spot
                moneyness = round(model_iv_object.strike * reciprocal_spot, 5)
                dte = int(round(model_iv_object.time_to_maturity * 365))
                key = (moneyness, dte)

                current_time = datetime.now()
                old_vol, old_time = self.vol_dict[key]

                # Incrementally calculate average implied volatility for the key
                updated_vol = (old_vol * self.counts[key] + model_iv_object.implied_volatility) / (self.counts[key] + 1)\
                    if old_time > current_time - timedelta(seconds=self.max_vsa_object_life_seconds) else model_iv_object.implied_volatility
                self.vol_dict[key] = (updated_vol, current_time)
                self.counts[key] = self.counts[key] + 1 if old_time > current_time - timedelta(seconds=self.max_vsa_object_life_seconds) else 1
            
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error in update_vol_dict_and_counts: {e}")

    def _remove_stale_entries(self) -> None:
        try:
            current_time = datetime.now()
            to_remove = [key for key, (vol, timestamp) in self.vol_dict.items()\
                if timestamp <= current_time - timedelta(seconds=self.max_vsa_object_life_seconds)]
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
