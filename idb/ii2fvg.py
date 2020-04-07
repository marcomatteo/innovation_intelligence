import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)

import pandas as pd
from sqlalchemy import create_engine, inspect

from utilities import Singleton

class II2FVG(metaclass = Singleton):

    def __init__(self):
        pass

if __name__ == '__main__':
    print("II2FVG class")
    interface = II2FVG()