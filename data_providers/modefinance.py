"""
23/10/2018

Classe per il data provider Modefinance per i ratings.

Innovation Intelligence in Python
Marco Matteo Buzzulini
"""

import pandas as pd
import numpy as np

from data_providers.dataProvider import DataProvider
from data_providers.dataProviderUtil import formatFiscalcodeColumn 

class Modefinance(DataProvider):
    source_type = "Ratings"
   
    def __init__(self, file_name):
        self.file_name = self.file_path + "ftp_modefinance/" + file_name
        self.sep = ';'
        self.open_source()
        self.df = formatFiscalcodeColumn(self.df, 'fiscal_code')

def main():
    print("Prova della classe Modefinance:")
    prova = Modefinance("MFSourceSample.csv")
    print(prova.df['final_rank'].value_counts())
    
if __name__ == '__main__':
    main()