# File contenente la classe Accredia 
# Rappresenta il data provider sulle certificazioni
# Data creazione: 20/08/2019

import pandas as pd
import numpy as np
from .dataProvider import DataProvider

class Accredia(DataProvider):
    source_type = "Certificazioni"
   
    def __init__(self, file_name):
        self.file_name = self.file_path + "Accredia/" + file_name
        self.sep = '|'
        self.open_source()
        # Gestisco le province di Napoli (NA)
        provincia = "istat_province_prcode"
        if provincia in self.df.columns:
            self.df[provincia].fillna('NA', inplace = True)

def main():
    print("Prova della classe Accredia:")
    prova = Accredia("20200203_accredia.csv")
    print(prova.df.head())
    
if __name__ == '__main__':
    main()