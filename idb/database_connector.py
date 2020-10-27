import pandas as pd
from collections import namedtuple
from sqlalchemy import create_engine, inspect

# from utilities import Singleton

class DatabaseConnector:

    dialect, driver = "mssql", "pyodbc"
    test_usr, data_usr = "I2FVGTestReader", "I2FVGDataReader"
    test_psw, data_psw = test_usr, data_usr
    test_db, data_db = "I2FVG_TEST", "I2FVG_DATA"

    Info = namedtuple("Info", ['name', 'unique', 'keys', 'foreign', 'columns'])

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
        """dialect+driver://username:password@host:port/database"""
        conn_begin = f"{self.dialect}+{self.driver}://"
        if self.inTest:
            return conn_begin + f"{self.test_usr}:{self.test_psw}@{self.test_db}"
            # return "mssql+pyodbc://I2FVGTestReader:I2FVGTestReader@I2FVG_TEST"
            # return "mssql+pyodbc://I2FVGTestReader:I2FVGTestReader@SQL2005.CONSORZIO.AREA.TRIESTE.IT/MSSQL05?driver=ODBC+Driver+17+for+SQL+Server"
        else:
            return conn_begin + f"{self.data_usr}:{self.data_psw}@{self.data_db}"
            # return "mssql+pyodbc://I2FVGDataReader:I2FVGDataReader@I2FVG_DATA_dev"

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

    def get_stats(self, table: str) -> Info:
        """
        Getting info from the table.
        
        Attributes
        ----------
        table: string
            name of the table in the DB 
    
        Return
        ------
        tbl_info: namedtuple
            >>> Info = namedtuple("Info", 
            ['name', 'unique', 'keys', 'foreign', 'columns'])
            
        Tuple with names for the specs of the selected table, names:
        
        - name: the table name
        
        - unique: return index information as a list of dicts with these keys:
            - name: the index’s name
            - column_names: list of column names in order
            - unique: boolean
            - dialect_options: dict of dialect-specific index options. May not be present for all dialects.
        
        - keys: return primary key information as a dictionary with these keys:
            - constrained_columns: a list of column names that make up the primary key
            - name: optional name of the primary key constraint.
            
        - foreign: return foreign key information as a list of dicts with these keys:
            - constrained_columns: a list of column names that make up the foreign key
            - referred_schema: the name of the referred schema
            - referred_table: the name of the referred table
            - referred_columns: a list of column names in the referred table that correspond to constrained_columns
            - name: optional name of the foreign key constraint.
            
        - columns: return column information as a list of dicts with these keys:
            - name: the column’s name
            - type: TypeEngine
            - nullable: boolean
            - default: the column’s default value
            - attrs: dict containing optional column attributes

        Raise
        -----
        ValueError: if the table name is not in the DB.
        """
        if table not in self.tables:
            raise ValueError("No table with this name")

        inspector = inspect(self.engine)
        tbl_info = self.Info(
            name = table,
            unique = inspector.get_indexes(table),
            keys = inspector.get_pk_constraint(table),
            foreign = inspector.get_foreign_keys(table), 
            columns = inspector.get_columns(table)
        )
        return tbl_info