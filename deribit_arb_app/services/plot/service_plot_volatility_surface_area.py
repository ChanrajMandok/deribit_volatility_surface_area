import time
import threading
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

from deribit_arb_app.services.managers.service_implied_volatility_queue_manager import ServiceImpliedVolatilityQueueManager

class ServicePlotVolatilitySurfaceArea(QtWidgets.QMainWindow):
    
    def __init__(self, volatility_manager: ServiceImpliedVolatilityQueueManager) -> None:
        super().__init__()
        self.volatility_manager = volatility_manager
        self.view = gl.GLViewWidget(self)
        self.scatter = gl.GLScatterPlotItem()
        self.view.addItem(self.scatter)
        self.setCentralWidget(self.view)
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.plot_volatility)
        self.plot_timer.start(20000)  # update every 20 seconds
        
    def plot_volatility(self):
        data_cache = self.volatility_manager.implied_volatility_dict.copy()  # copy data to avoid conflicts
        strikes, maturities, vols = zip(*[(k[0], k[1], v) for k, v in data_cache.items()])
        data = np.empty(len(strikes), dtype=[('position', float, 3)])
        data['position'] = list(zip(strikes, maturities, vols))
        self.scatter.setData(pos=data['position'])