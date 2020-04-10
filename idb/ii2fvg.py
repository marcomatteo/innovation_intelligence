from utilities import ROOT, Singleton
import pandas as pd
from sqlalchemy import create_engine, inspect

from utilities import Singleton

class II2FVG(metaclass = Singleton):

    def __init__(self, test=True):
        self.test = test

    @property
    def mod(self):
        if self.test:
            return "Test"
        else:
            return "Data"

    @property
    def connessione(self):
        if self.test:
            return "mssql+pyodbc://I2FVGTestReader:I2FVGTestReader@I2FVG_TEST"
        else:
            return "mssql+pyodbc://I2FVGDataReader:I2FVGDataReader@I2FVG_DATA_dev"

if __name__ == '__main__':
    print("II2FVG class")
    interface = II2FVG()