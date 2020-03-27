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
        self.df = self.get_merge_tables()
    
    def get_merge_tables(self):
        """
        Unione delle tabelle 'DATA_Certificazione' e 'SVC_Certificazione'
        """
        convert_type = {'RF_Certificazione':'float64'}
        df = self.tbl_df['certificazioni'].astype(convert_type).merge(
                    self.tbl_df['tipologie'], 
                    how='left', 
                    left_on='RF_Certificazione', 
                    right_on='ID_Certificazione'
            )
        return df

    def get_certificazioni(self):
        """
        Metodo che permette di estrarre le singole tipologie
        di certificazioni presenti nel DB
        """
        certificazioni_series = self.df['CodiceCertificazione'].value_counts()
        certificazioni_series = certificazioni_series.drop(labels=' No certificazioni', axis=0)
        certificazioni_list = certificazioni_series.index.map(lambda x: str(x).strip()).tolist()
        return certificazioni_list
    
    def set_cleaned_merged_table(self):
        """
        Pulizia delle colonne non necessarie
        """
        cols_list = [
            'ID_DataCertificazione', 'RF_Certificazione',
            'RF_Importazione', 'ID_Certificazione', 
            'RF_TipoCertificazione', 'DataInsert'
        ]
        self.df.drop(columns=cols_list, inplace=True)

def main():
    print("Prova della classe Certificazione:")
    prova = Certificazione(test = True)
    print("Stampa della tabella merged:\n", prova.df.head())
    
if __name__ == '__main__':
    main()