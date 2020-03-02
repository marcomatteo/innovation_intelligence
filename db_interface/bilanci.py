"""
Creata il: 28/10/2019

Classe per la tabella DATA_Bilanci di Innovation Intelligence.

Innovation Intelligence in Python
Marco Matteo Buzzulini
"""
import os

path = f"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts"
try:
    os.chdir(path)
    #print(f"Current dir: {os.getcwd()}")
except:
    print("Can't load the right dir")    

from innovation_intelligence.db_interface.i2fvg import I2FVG
from collections import defaultdict

class Bilanci(I2FVG):
    # Costanti
    _names = {  'bilancio': 'DATA_Bilancio',
                'ultimo': 'DATA_UltimoBilancio',
                'ultimoDisp': 'DATA_UltimoBilancioDisponibile'}

    def __init__(self, table = None, inTest = True, default = 'bilancio'):
        super().__init__(inTest = inTest)
        self.open_tables(name=table)
        if table is not None:
            self.df = self.tbl_df[table]
            self.info = self.tbl_info[table]
        else:
            self.df = self.tbl_df[default]
            self.info = self.tbl_info[default]

    def indicatori_classe(self):
        pass


def main():
    print("Prova della classe Bilanci:")
    prova = Bilanci(table='bilancio')
    print(prova.info.keys)


if __name__ == '__main__':
    main()