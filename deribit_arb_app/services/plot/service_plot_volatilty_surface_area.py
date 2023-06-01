import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from typing import Dict, List
from scipy.interpolate import griddata

from deribit_arb_app.enums.enum_option_type import EnumOptionType
from deribit_arb_app.model.indicator_models.model_indicator_bsm_implied_volatilty import ModelIndicatorBsmImpliedVolatility

    ######################################################################################
    # Service Plots Volatility Surface Area from Indicator Bsm Implied Volatilty objects #
    ######################################################################################

class ServicePlotVolatilitySurfaceArea():

    def __init__(self):
        plt.ion()
        self.fig = plt.figure(figsize=(12, 12))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('Strike Price')
        self.ax.set_ylabel('Days to Expiry')
        self.ax.set_zlabel('Volatilty')
        plt.rcParams.update({'font.size': 12})
        self.ax.view_init(elev=30, azim=120)
        self.surface = None

    def update_plot(self, implied_vol_dict_live:Dict[str, List[ModelIndicatorBsmImpliedVolatility]]):
        # Initialize data arrays
        all_strikes = []
        all_maturities = []
        all_vols = []

        for key, data in implied_vol_dict_live.items():
            for iv_model_object in data:
                dte = int(round(float(iv_model_object.time_to_maturity) * 365, 0))
                all_maturities.add(dte)
                all_strikes.add(float(iv_model_object.strike))
                all_vols.add(float(iv_model_object.implied_volatilty))
                
        # Clear plot
        if self.surface:
            self.surface.remove()

        # Recreate grid for surface plot
        strike_prices = np.linspace(min(all_strikes), max(all_strikes), 100)
        days_to_expiry = np.linspace(min(all_maturities), max(all_maturities), 100)
        X, Y = np.meshgrid(strike_prices, days_to_expiry)
        Z = griddata((all_strikes, all_maturities), all_vols, (X, Y), method='linear')

        # Update surface plot
        self.surface = self.ax.plot_surface(X, Y, Z, cmap=cm.inferno)
        plt.title(f" Okx Volatility Surface Area")
        self.fig.colorbar(self.surface, shrink=0.5, aspect=5)

    def start_animation(self, implied_vol_dict_live, interval=1000):
        # implied_vol_dict_live is your live data stream, interval is the delay between updates in ms
        ani = animation.FuncAnimation(self.fig, self.update_plot, fargs=(implied_vol_dict_live,), interval=interval, blit=False)
        plt.show()