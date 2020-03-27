"""

certificazione.py
20/08/2019

Classe Certificazione che fa riferimento alle tabelle di Innovation Intelligence sulle certificazione (ISO 9100, etc.)

"""
import sys
sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")
import os
import pandas as pd
from db_interface import I2FVG

class Certificazione(I2FVG):
    # Costanti
    _names = {
        'certificazioni': 'DATA_Certificazione',
        'tipologie': 'SVC_Certificazione'
    }
    
    def __init__(self, test=True, table=None):
        """
        Classe Certificazione rappresenta le tabelle di Innovation Intelligence sul DB.
        """
        super().__init__(inTest = test)
        self.open_tables(name=table)
        self.df = self.tbl_df['certificazioni'].astype(
            {'RF_Certificazione':'float64'}).merge(
                    self.tbl_df['tipologie'], 
                    how='left', 
                    left_on='RF_Certificazione', 
                    right_on='ID_Certificazione'
            )

def main():
    print("Prova della classe Certificazione:")
    prova = Certificazione(test = True)
    print("Stampa della tabella merged:\n", prova.df.head())
    
if __name__ == '__main__':
    main()