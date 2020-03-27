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
    """
    Oggetto di I2FVG per le certificazioni di qualità,
    certificazioni ambientali ed energetiche, 
    certificazioni di gestione della sicurezza

    Le certificazioni sono salvate sul DB in due tabelle:

    - DATA_Certificazione: per azienda

    - SVC_Certificazione: per certificazione

    Ogni istanza carica le tabelle e salva la loro unione
    in un'unica rappresentazione tabellare.

    Attributi:
    ----------
        test: str 
        Modalità di apertura del test

        engine: SqlAlchemy obj
        Attributo utilizzato per interagire con il connettore del DB

        tables: list
        Lista di tutte le tabelle presenti nel DB

        _names: dict of str
        Dizionario in cui sono inserite le tabelle del DB sulle Certificazioni
        Le key sono delle abbreviazioni utilizzate anche in tbl_df e tbl_info

        tbl_df: dict of pandas.DataFrame
        Dizionario delle tabelle del DB sulle Certificazioni
        Ogni tabella ha come key del dict la corrispondente 
        nel dict _names.keys()
        
        tbl_info: dict of subclass Info (obj created with namedtuple) 
        Dizionario delle informazioni delle tabelle del DB 
        sulle Certificazioni
        Ogni tabella ha come key del dict la corrispondente 
        nel dict _names.keys()

        df: pandas.DataFrame
        Rappresentazione unica delle informazioni sul DB in Pandas

    Metodi:
    -------
        __init__(self, file_name):
        Inizializzatore di classe che apre apre 
        le tabelle contenute in _names e salva in df 
        la loro unione in un unico pandas.DataFrame

        def set_cleaned_merged_table(self):
        Metodo che permette di eliminare le colonne di sistema
        che non riguardano le Certificazioni

        def get_merged_tables(self) -> pd.DataFrame:
        Metodo per ottenere l'unione delle due tabelle 
        in un pandas.DataFrame

        def get_certificazioni(self) -> list:
        Metodo che permette di estrarre le singole tipologie 
        di certificazioni presenti nel DB
    """

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
        self.df = self.get_merged_tables()

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
    
    def get_merged_tables(self) -> pd.DataFrame:
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

    def get_certificazioni(self) -> list:
        """
        Metodo che permette di estrarre le singole tipologie
        di certificazioni presenti nel DB
        """
        certificazioni_series = self.df['CodiceCertificazione'].value_counts()
        certificazioni_series = certificazioni_series.drop(labels=' No certificazioni', axis=0)
        certificazioni_list = certificazioni_series.index.map(lambda x: str(x).strip()).tolist()
        return certificazioni_list
    

def main():
    print("Prova della classe Certificazione:")
    prova = Certificazione(test = True)
    print("Stampa della tabella merged:\n", prova.df.head())
    
if __name__ == '__main__':
    main()