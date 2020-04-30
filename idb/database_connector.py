import pandas as pd
from sqlalchemy import create_engine, inspect

# from utilities import Singleton

class DatabaseConnector:

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
            # return "mssql+pyodbc://I2FVGTestReader:I2FVGTestReader@SQL2005.CONSORZIO.AREA.TRIESTE.IT/MSSQL05?driver=ODBC+Driver+17+for+SQL+Server"
        else:
            return "mssql+pyodbc://I2FVGDataReader:I2FVGDataReader@I2FVG_DATA_dev"

    def get_dataframe_from_table(self, table_name: str, *args, **kwargs) -> pd.DataFrame:
        if table_name in self.tables:
            df = pd.read_sql_table(
                    table_name, 
                    con = self.engine, 
                    *args, **kwargs
                )
        else:
            raise KeyError(f"Invalid table name! No {table_name} in DB!")

        return df
    
    def get_dataframe_from_query(self, query: str, *args, **kwargs) -> pd.DataFrame:
        result = pd.read_sql_query(query, self.engine, *args, **kwargs)
        return result

if __name__ == '__main__':
    ii = DatabaseConnector()
    print(len(ii.tables))