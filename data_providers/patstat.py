"""

patstat.py
20/08/2019

Classe Patstat per il provider di dati EPO Patstat

"""

from sqlalchemy import create_engine, inspect
from .dataProvider import Data

class Patstat(Data):

    connessione = "mssql+pyodbc://patstatqa:PatStaT.Q4.Usr@patstat"

    def __init__(self):
        self.engine = create_engine(self.connessione)
        self.inspect = inspect(self.engine)
        self.table_names = self.inspect.get_table_names()
        self.schema_names = self.inspect.get_schema_names()

    def print_stats(self, tbl=None):
        """
        Method used for print the db tables. 
        Input:
        - tbl [String]: the name of the specific table to print.
        
        Return: Nothing
        """
        print("Schema names: {}".format(self.schema_names))
        if tbl is not None:
            if tbl in self.table_names:
                print("\nTable {} informations:".format(tbl))
                columns = self.inspect.get_columns(tbl)
                print("Columns: \n{}".format(columns))
                keys = self.inspect.get_pk_constraint(tbl)
                print("Keys: \n{}".format(keys))
            else:
                print("\nInvalid table name.")
        else:
            print("\nTable names: {}".format(self.table_names))

def main():
    print("Prova della classe PATSTAT:")
    prova = Patstat()
    prova.print_stats("tls201_appln")
    del prova

if __name__ == '__main__':
    main()
