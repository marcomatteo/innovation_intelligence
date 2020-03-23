"""
Creata il: 20/08/2019

Superclasse per tutte le tabelle di Innovation Intelligence.

Innovation Intelligence in Python
Marco Matteo Buzzulini
"""
from sqlalchemy import create_engine, inspect
from collections import namedtuple
import pandas as pd

class I2FVG(object):
    """
    Innovation Intelligence class.
    Allows to access to the I2FVG DB in test or production mode.
    
    
    Attributes
    ----------
        test: str 
            used in the init method for mode selection
        engine: SqlAlchemy obj
            used for setting up the db connection
        tables: list
            with all the db tables available
        tbl_df: dict of pandas.DataFrame
            the place where you can find the tables in pandas DataFrame with
            short name as dict key
        tbl_info: dict of subclass Info (obj created with namedtuple) 
            the place where you can find the info related to the tbl_df key
    
    Methods
    -------
    
    """
    # Colleziona tutte le info per la tabella
    Info = namedtuple(
        "Info", 
            ['name', 'unique', 'keys', 'foreign', 'columns']
        )
    # info per unit testing 
    InfoCols = namedtuple(
        "InfoCols",
            ['names', 'types', 'lengths', 'nullables']
        )
    # codifica dei dataframes -> tbl_df
    _names = dict()

    def __init__(self, inTest = True):
        """
        Parameters
        ----------
        inTest: boolean, default True
            access to the db in the test mode if True, 
            otherwise use the production mode. 

        Returns
        -------
        None.

        """
        self.test = inTest
        # if test mode is not working try the other mode
        try:
            self.engine = create_engine(self.connessione)
        except ConnectionError:
            # Testing DATA mode
            self.test = not inTest
            self.engine = create_engine(self.connessione)
        
        self.tables = self.engine.table_names()
        data_tbl_names = [ 
            name 
            for name in self.tables
            if name.startswith('DATA_')
        ]
        data_names = [ 
            x.split('DATA_')[1]
            for x in data_tbl_names
        ]
        # Only the DATA_ tables with a short name as key
        self.tbl_data = {
            name: tbl_name
            for name, tbl_name
            in zip(data_names, data_tbl_names)
        }
        self.tbl_df = dict()
        self.tbl_info = dict()

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
             
    @classmethod
    def set_primary_keys(cls, info, df):
        """
        Funzione da utilizzare per impostare la chiave primaria di una tbl.
        """
        # DataFrame index keys
        keys = info.keys[0]['column_names']
        # Setting the index from tbl_info
        if len(keys) == 0:
            keys = info.key['constrained_columns']
        return df.set_index(keys)
    
    @classmethod
    def get_refferedTables(cls, db_class ):
        """
        Metodo che ritorna la lista delle tabelle collegate ad una classe
        """
        tables = list()
        name = db_class.tbl_info.keys()[0]
        for fk in db_class.tbl_info[name].foreign:
            tables.append(fk['referred_table'])
        return tables

    def get_stats(self, table: str):
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
            raise ValueError("No table in the DB with this name.\
                             Check the string")
        inspector = inspect(self.engine)
        tbl_info = self.Info(
            name = table,
            unique = inspector.get_indexes(table),
            keys = inspector.get_pk_constraint(table),
            foreign = inspector.get_foreign_keys(table), 
            columns = inspector.get_columns(table)
        )
        return tbl_info
    
    def open_tables(self, name=None, nrows=None):
        tbl_to_open = self._names
        
        # Opening mode selection
        if name is not None:
            if name in tbl_to_open:
                tbl_to_open = {name: self._names.get(name)}
            else:
                raise AttributeError('Wrong table to open')
       
        # Load specific tables
        for key, tbl in tbl_to_open.items():
            if tbl in self.tables:
                # Get tbl info for index col
                self.tbl_info[key] = self.get_stats(tbl)
                # Load DF
                self.tbl_df[key] = pd.read_sql_table(
                    tbl, con = self.engine)
                print("Aperta tabella in tbl_df['{}'] = '{}' in {}".format(
                    key, tbl, self.mod
                ))
            else:
                raise AttributeError('Wrong table in _names to open')
    

def main():
    print("Prova Classe I2FVG:")
    try:
        prova = I2FVG()
    except ConnectionError:
        print("Errore di connessione al DB.")
    table = 'DATA_Bilancio'
    info = prova.get_stats(table)
    print(info.keys['constrained_columns'])

if __name__ == '__main__':
    main()
