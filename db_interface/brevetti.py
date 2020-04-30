"""
Creata il: 23/10/2019

Classe per le tabelle DATA_Brevetti_Impresa e DATA_Brevetti_Brevetto.

Innovation Intelligence in Python
Marco Matteo Buzzulini
"""
import pandas as pd
from db_interface import I2FVG

class Brevetti(I2FVG):
    # Nomi tabelle della classe
    _names = { 
        'impresa': "DATA_Brevetti_Impresa",
        'brevetto': "DATA_Brevetti_Brevetto",
        'ipc': 'DATA_Brevetti_Brevetto_CodiceIPC',
        'matching': 'SVC_Imprese_Match'
    }

    def __init__(self, inTest = True):
        # Apro la connessione con il DB
        super().__init__(inTest = inTest)
        # Apro le tabelle
        self.open_tables()
        # Effettuo il merge tra le tabelle
        self.df = self.tbl_df['impresa'].merge(
            self.tbl_df['brevetto'],
            left_on = 'RF_' + self._names['brevetto'],
            right_on = 'ID_' + self._names['brevetto'],
            how = 'inner'
        )#.merge(self.tbl_df['ipc'], on = 'ID_' + self._names['ipc'])
        print(f"Aperta tabella Brevetti in {self.mod}")

def main():
    print("Prova della classe Brevetti:")
    prova = Brevetti()
    del prova

if __name__ == '__main__':
    main()