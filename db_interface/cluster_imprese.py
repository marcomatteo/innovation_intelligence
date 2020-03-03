"""
Creata il: 12/11/2019

Classe per la tabella DATA_Cluster_Impresa di Innovation Intelligence.

Innovation Intelligence in Python
Marco Matteo Buzzulini
"""

from .i2fvg import I2FVG
import pandas as pd

class Clusters(I2FVG):
    _names = {
        'clusters': 'DATA_Cluster_Impresa'
    }

    def __init__(self, inTest = True):
        super().__init__(inTest = inTest)
        self.open_tables()
        self.df = self.tbl_df['clusters']

def main():
    print("Prova della classe Coselag:")
    prova = Clusters()
    print(prova.df.head())
    
if __name__ == '__main__':
    main()