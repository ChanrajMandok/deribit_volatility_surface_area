import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import asyncio
import numpy as np
from scipy.interpolate import griddata
from matplotlib import cm
from IPython.terminal.pt_inputhooks import register

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

    def update_plot(self, implied_vol_queue: asyncio.Queue):
        # Initialize data arrays
        all_strikes = []
        all_maturities = []
        all_vols = []

        while not implied_vol_queue.empty():
            iv_model_object = implied_vol_queue.get_nowait()
            dte = int(round(float(iv_model_object.time_to_maturity) * 365, 0))
            all_maturities.append(dte)
            all_strikes.append(float(iv_model_object.strike))
            all_vols.append(float(iv_model_object.implied_volatilty))
            
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

    def start_animation(self, implied_vol_queue, interval=1000):
        ani = FuncAnimation(self.fig, self.update_plot, fargs=(implied_vol_queue,), interval=interval, blit=False)
        plt.show()

    # Enable asyncio event loop support for matplotlib
    @register
    def inputhook(context):
        asyncio.get_event_loop().run_until_complete(context.input_is_ready())
