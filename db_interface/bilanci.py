"""
Creata il: 28/10/2019

Classe per la tabella DATA_Bilanci di Innovation Intelligence.

Innovation Intelligence in Python
Marco Matteo Buzzulini
"""
import pandas as pd
import numpy as np
import db_interface
from collections import defaultdict

class Bilanci(db_interface.I2FVG):
    # Costanti
    _names = {  'bilancio': 'DATA_Bilancio',
                'ultimo': 'DATA_UltimoBilancio',
                'ultimoDisp': 'DATA_UltimoBilancioDisponibile'}

    def __init__(self, inTest = True):
        super().__init__(inTest = inTest)
        for name, tbl in self._names.items():
            self.tbl_info[name] = self.get_stats(tbl)

    def indicatori_classe(self):
        pass
    
    def open_tables(self, table = None, query = None):
        """
        Metodo che permette di aprire le tabelle di Bilancio \
        in due modalità:

            1: Tramite il nome codificato delle tabelle presenti \
                come key nel dict _names
            
            2: Tramite query SQL direttamente al DB
        """
        # Opening mode selection
        if table:
            self._open_tables(tables=table)
        elif query:
            try:
                self.df = pd.read_sql_query(
                    query,
                    self.engine
                )
            except:
                raise ValueError("Invalid query")
        else:
            try:
                self._open_tables()
            except AttributeError:
                print("Fail to open tables. \
                Change the tables in the attribute self._names")
    
    def _open_tables(self, tables: list = None):
        tables_to_open = dict()

        if tables:
            for table in tables:
                if table in self._names:
                    tables_to_open[table] = self._names.get(table)
                else:
                    raise AttributeError('Wrong table to open')

        # Load specific tables
        for key, tbl in tables_to_open.items():
            if tbl in self.tables:
                # Load DF
                self.tbl_df[key] = pd.read_sql_table(
                    tbl, con = self.engine)
                print("Aperta tabella in tbl_df['{}'] = '{}' in {}".format(
                    key, tbl, self.mod
                ))
            else:
                raise AttributeError('Wrong table in _names to open')

def main():
    print("File bilanci.py")
    print("Inizializzare Bilanci e utilizzare il metodo open_tables per accedere alle tbl")


if __name__ == '__main__':
    main()