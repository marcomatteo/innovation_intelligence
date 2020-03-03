"""
Creata il: 23/10/2019

Classe per le tabelle "DATA_FinanziamentiUE_Impresa" ...

Innovation Intelligence
Marco Matteo Buzzulini
"""
import pandas as pd

from .i2fvg import I2FVG

class Finanziamenti(I2FVG):
    # Nomi tabelle della classe
    _names = {
        'impresa': "DATA_FinanziamentiUE_Impresa"
    }

    def __init__(self, inTest=True):
        # Apro la connessione con il DB
        super().__init__(inTest = inTest)
        df_names = dict()
        for key, tbl in self._names.items():
            df_names[key] = pd.read_sql_table(
                tbl, con=self.engine,
                index_col=('ID_' + tbl)
            )
        self.df = df_names['impresa']
        print("Aperta tabella Finanziamenti in {}".format(self.mod))

if __name__ == '__main__':
    print("Prova della classe Finanziamenti:")
    prova = Finanziamenti()