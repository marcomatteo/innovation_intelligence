import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)

import numpy as np
import pandas as pd

from setup import Singleton

class DataProvider(metaclass = Singleton):

    def __init___(self):
        pass

if __name__ == '__main__':
    print("DataProvider.py")