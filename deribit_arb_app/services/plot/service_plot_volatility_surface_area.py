import sys
import datetime

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer


class ServicePlotVolatilitySurfaceArea(QtWidgets.QMainWindow):
    
    def __init__(self) -> None:
        input_dict = {'25750.0-put': {'value': 0.99335, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 40, 135797), 'time_to_maturity': 0.0015}, '26000.0-put': {'value': 0.34012, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 42, 337926), 'time_to_maturity': 0.0837},
                      '26250.0-call': {'value': 1.20666, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 41, 116864), 'time_to_maturity': 0.0043}, '26250.0-put': {'value': 1.27952, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 40, 499105), 'time_to_maturity': 0.0015},
                      '26500.0-put': {'value': 1.32488, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 40, 604644), 'time_to_maturity': 0.0015}, '27000.0-put': {'value': 1.32049, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 40, 697850), 'time_to_maturity': 0.0015},
                      '27500.0-put': {'value': 1.38213, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 40, 801705), 'time_to_maturity': 0.0015}, '25750.0-call': {'value': 2.68007, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 40, 906873), 'time_to_maturity': 0.0043},
                      '26000.0-call': {'value': 2.28091, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 41, 13487), 'time_to_maturity': 0.0043}, '22000.0-put': {'value': 3.0682, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 41, 333577), 'time_to_maturity': 0.007},
                      '25000.0-call': {'value': 3.54888, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 41, 457594), 'time_to_maturity': 0.007}, '30000.0-put': {'value': 4.26623, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 41, 566713), 'time_to_maturity': 0.007},
                      '36000.0-put': {'value': 2.68037, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 41, 695703), 'time_to_maturity': 0.007}, '22000.0-call': {'value': 4.43031, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 37, 838600), 'time_to_maturity': 0.0837},
                      '28000.0-put': {'value': 0.34348, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 38, 253226), 'time_to_maturity': 0.0837}, '29000.0-put': {'value': 0.41947, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 38, 351047), 'time_to_maturity': 0.0837},
                      '14000.0-put': {'value': 4.23702, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 29, 851872), 'time_to_maturity': 0.2562}, '15000.0-put': {'value': 2.43418, 'timestamp': datetime.datetime(2023, 9, 26, 19, 35, 50, 660797), 'time_to_maturity': 0.2562},
                      '16000.0-call': {'value': 0.41362, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 38, 724172), 'time_to_maturity': 0.2562}, '20000.0-put': {'value': 2.65359, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 3, 671152), 'time_to_maturity': 0.2562},
                      '24000.0-put': {'value': 1.99088, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 21, 605664), 'time_to_maturity': 0.2562}, '25000.0-put': {'value': 2.45334, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 34, 771182), 'time_to_maturity': 0.2562},
                      '35000.0-put': {'value': 4.28121, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 17, 730824), 'time_to_maturity': 0.2562}, '40000.0-put': {'value': 4.36317, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 13, 442633), 'time_to_maturity': 0.2562},
                      '32000.0-call': {'value': 2.67485, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 4, 665228), 'time_to_maturity': 0.5055}, '35000.0-call': {'value': 0.6623, 'timestamp': datetime.datetime(2023, 9, 26, 19, 36, 13, 380142), 'time_to_maturity': 0.5055},
                      '38000.0-call': {'value': 1.79954, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 27, 110136), 'time_to_maturity': 0.5055}, '40000.0-call': {'value': 1.44145, 'timestamp': datetime.datetime(2023, 9, 26, 19, 35, 52, 100040), 'time_to_maturity': 0.5055},
                      '18000.0-put': {'value': 3.19957, 'timestamp': datetime.datetime(2023, 9, 26, 19, 37, 41, 211746), 'time_to_maturity': 0.007}}
