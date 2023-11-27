import traceback

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from deribit_arb_app.services import logger
from matplotlib.animation import FuncAnimation

    ################################################
    # Service Plots Volatility Surface Area Object #
    ################################################

class ServicePlotVolatilitySurfaceArea():
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(12, 12))
        self.surface = None
        self.iv_array = None
        self.ttm_array = None
        self.moneyness_array = None


    def create_plot(self,
                    iv_array: np.ndarray,
                    ttm_array: np.ndarray,
                    moneyness_array: np.ndarray) -> None:
        try:
            self.iv_array = iv_array
            self.ttm_array = ttm_array
            self.moneyness_array = moneyness_array
            
            self.surface = self.ax.plot_surface(moneyness_array, ttm_array, iv_array, cmap=cm.inferno)
            self.ax.set_xlabel('Moneyness')
            self.ax.set_ylabel('Days to Expiry')
            self.ax.set_zlabel('Volatility')
            plt.title("Volatility Surface Area")
            self.fig.colorbar(self.surface, shrink=0.5, aspect=5)
            plt.rcParams.update({'font.size': 12})
            self.ax.view_init(elev=30, azim=120)
            
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                      f"Stack trace: {traceback.format_exc()}")


    def update_plot(self, 
                    iv_array: np.ndarray,
                    ttm_array: np.ndarray, 
                    moneyness_array: np.ndarray) -> plt.Artist:
        try:
            self.iv_array = iv_array
            self.ttm_array = ttm_array
            self.moneyness_array = moneyness_array
            
            if self.surface:
                self.surface.remove()  # remove the old surface
            self.surface = self.ax.plot_surface(moneyness_array, ttm_array, iv_array, cmap=cm.inferno)
            return self.surface
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                      f"Stack trace: {traceback.format_exc()}")


    def animate(self, i):
        try:
            # Ensure these arrays are updated to the most recent before animation frame update
            return (self.update_plot(self.iv_array, self.ttm_array, self.moneyness_array), )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                      f"Stack trace: {traceback.format_exc()}")


    def show(self):
        try:
            anim = FuncAnimation(self.fig, self.animate, interval=100, save_count=100, blit=True)
            plt.show(block=False)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}: Error: {str(e)}. " \
                                                      f"Stack trace: {traceback.format_exc()}")