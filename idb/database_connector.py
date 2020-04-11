from utilities import ROOT, Singleton
import pandas as pd
from sqlalchemy import create_engine, inspect

# from utilities import Singleton

class DatabaseConnector():

    def __init__(self, inTest=True):
        self.inTest = inTest

    @property
    def mod(self):
        if self.inTest:
            return "Test"
        else:
            return "Data"

    @property
    def connection_string(self):
        if self.inTest:
            return "mssql+pyodbc://I2FVGTestReader:I2FVGTestReader@I2FVG_TEST"
        else:
            return "mssql+pyodbc://I2FVGDataReader:I2FVGDataReader@I2FVG_DATA_dev"