# File contenente la classe Accredia 
# Rappresenta il data provider sulle certificazioni
# Data creazione: 20/08/2019
import sys
sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")

import pandas as pd
import numpy as np
import os

from .dataProvider import DataProvider

class Accredia(DataProvider):
    source_type = "Certificazioni"
   
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_path = self.file_path + r"Accredia/" + self.file_name
        self.sep = '|'
        try:
            self.open_source()
        except TypeError:
            print("Wrong file extension!")
        except FileNotFoundError:
            print("File not found! Check the path")

    def open_source(self):
        assert self.file_ext.startswith("csv"), TypeError("Wrong file extension!")
        assert os.path.isfile(self.file_path), FileNotFoundError("File not found!")

        self.df = pd.read_csv(
                self.file_path, 
                sep=self.sep, 
                dtype=object, 
                keep_default_na=False, 
                na_values=""
            )

def main():
    print("Prova della classe Accredia:")
    prova = Accredia("20200203_accredia.csv")
    print(prova.df.head())
    
if __name__ == '__main__':
    main()