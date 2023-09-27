import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from collections import defaultdict
from scipy.interpolate import griddata, RegularGridInterpolator

from deribit_arb_app.services import logger
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatility import \
                                                         ModelIndicatorBsmImpliedVolatility

    ################################################
    # Service Plots Volatility Surface Area Object #
    ################################################

class ServicePlotVolatilitySurfaceArea():
    
    def __init__(self) -> None:
        self.surface = None
        self.X = None
        self.Y = None
        self.Z = None
        self.interpolator = None
    
    def plot(self, model_iv_objects: list[ModelIndicatorBsmImpliedVolatility]) -> None:
        
        # Initialize data arrays and defaultdict
        vol_dict = defaultdict(float)
        counts = defaultdict(int)
        
        for model_iv_object in model_iv_objects:
            # Calculations
            reciprocal_spot = 1.0 / model_iv_object.spot
            moneyness = round(model_iv_object.strike * reciprocal_spot, 5)
            dte = int(round(model_iv_object.time_to_maturity * 365))
            
            key = (moneyness, dte)
            
            # Incrementally calculate average implied volatility for the key
            vol_dict[key] = (vol_dict[key] * counts[key] + model_iv_object.implied_volatility) / (counts[key] + 1)
            counts[key] += 1
        
        all_moneyness, all_maturities, all_vols = zip(*[(moneyness, dte, vol) for (moneyness, dte), vol in vol_dict.items()])
        
        # Create grid for surface plot using numpy arrays
        moneyness_values = np.linspace(min(all_moneyness), max(all_moneyness), 200)
        days_to_expiry = np.linspace(min(all_maturities), max(all_maturities), 200)
        self.X, self.Y = np.meshgrid(moneyness_values, days_to_expiry)
        self.Z = griddata((all_moneyness, all_maturities), all_vols, (self.X, self.Y), method='linear')
        
        # Create surface plot
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(111, projection='3d')
        self.surface = ax.plot_surface(self.X, self.Y, self.Z, cmap=cm.inferno)
        ax.set_xlabel('Moneyness')
        ax.set_ylabel('Days to Expiry')
        ax.set_zlabel('Volatility')
        plt.title("Volatility Surface Area")
        fig.colorbar(self.surface, shrink=0.5, aspect=5)
        plt.rcParams.update({'font.size': 12})
        ax.view_init(elev=30, azim=120)
        plt.show(block=False)
        
    # def interpolate(self, moneyness, dte):
    #     if self.interpolator is not None:
    #         return self.interpolator([[moneyness, dte]])
    #     else:
    #         raise ValueError("Interpolator has not been initialized, please run the plot method first.")
    #         self.interpolator = RegularGridInterpolator((moneyness_values, days_to_expiry), self.Z, bounds_error=False, fill_value=None)