from utilities import ROOT, Singleton
import pandas as pd
from sqlalchemy import create_engine, inspect

# from utilities import Singleton

class DatabaseConnector():

    def __init__(self, inTest=True):
        self.inTest = inTest
        self.engine = create_engine(self.connection_string)
        self.tables = self.engine.table_names()

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

    def open_table(self, table_name):
        pass

if __name__ == '__main__':
    ii = DatabaseConnector()
    print(len(ii.tables))