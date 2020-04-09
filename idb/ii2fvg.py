from utilities import ROOT, Singleton
import pandas as pd
from sqlalchemy import create_engine, inspect

from utilities import Singleton

class II2FVG(metaclass = Singleton):

    def __init__(self):
        pass

if __name__ == '__main__':
    print("II2FVG class")
    interface = II2FVG()