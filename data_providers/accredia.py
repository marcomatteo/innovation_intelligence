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
    """
    Data Provider per le certificazioni di qualità,
    certificazioni ambientali ed energetiche, 
    certificazioni di gestione della sicurezza

    Il file fonte è generalmente un file csv.

    Il file fonte ci viene inviato con un'insieme di 
    certificazioni relative ad un numero di aziende
    superiore a quello di I2FVG. E' necessario quindi
    effettuare una selezione dei codici fiscali per poter
    effettuare comparazioni del file caricato.

    Attributi:
    ----------
        file_name: str
        Nome del file aperto con estensione

        file_path: str
        Percorso completo del file aperto

        sep: str
        separatore di colonna del file csv

        df: pandas.DataFrame
        Rappresentazione del file csv in Pandas

    Metodi:
    -------
        __init__(self, file_name):
        Inizializzatore di classe che apre il file
        passato come argomento aggiungendone file_path
        da DataProvider

        def set_DataFrame(self):
        Metodo per aprire il file csv in file_path

        def set_selected_fiscalcodes(self, cf_list: list):
        Metodo per selezionare dal file fonte solo i
        codici fiscali di I2FVG

        def set_renamed_df(self):
        Metodo per rinominare il df con le colonne usate 
        in I2FVG

        get_DataFrame(self): -> pd.DataFrame
        Metodo per aprire il file csv in file_path

        def get_renamed_df(self): -> pd.DataFrame
        Metodo per ottenere il df con le colonne rinominate

        def get_certificazioni(self) -> list:
        Metodo per ottenere la lista delle certificazioni
        del file. Consiglio di utilizzo dopo aver applicato 
        set_selected_fiscalcodes
    """
    source_type = "Certificazioni"
   
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_path = self.file_path + r"Accredia/" + self.file_name
        self.sep = '|'
        try:
            self.df = self.get_DataFrame()
        except TypeError:
            print("Wrong file extension!")
        except FileNotFoundError:
            print("File not found! Check the path")

    def set_DataFrame(self):
        assert self.file_ext.startswith("csv"), TypeError("Wrong file extension!")
        assert os.path.isfile(self.file_path), FileNotFoundError("File not found!")

        self.df = pd.read_csv(
                self.file_path, 
                sep=self.sep, 
                dtype=object, 
                keep_default_na=False, 
                na_values=""
            )

    def set_selected_fiscalcodes(self, cf_list: list):
        """
        Metodo per selezionare i codici fiscali nel df
        """
        cond = self.df.iloc[:, 0].isin(cf_list)
        self.df = self.df.loc[cond]

    def set_renamed_df(self):
        """Metodo per rinominare le colonne come sono importate in DB"""
        rename_dict = {
            'fiscalcode': 'CF',
            'istat_province_prcode': 'PV',
            'regulation': 'CodiceCertificazione'
        }
        self.df.rename(columns=rename_dict, inplace=True)

    def get_DataFrame(self) -> pd.DataFrame:
        assert self.file_ext.startswith("csv"), TypeError("Wrong file extension!")
        assert os.path.isfile(self.file_path), FileNotFoundError("File not found!")

        df = pd.read_csv(
                self.file_path, 
                sep=self.sep, 
                dtype=object, 
                keep_default_na=False, 
                na_values=""
            )

        return df

    def get_renamed_df(self) -> pd.DataFrame:
        """Metodo per rinominare le colonne come sono importate in DB"""
        rename_dict = {
            'fiscalcode': 'CF',
            'istat_province_prcode': 'PV',
            'regulation': 'CodiceCertificazione'
        }
        return self.df.rename(columns=rename_dict).copy()

    def get_certificazioni(self) -> list:
        """
        Metodo che permette di estrarre le singole tipologie
        di certificazioni presenti nel DB
        """
        certificazioni_series = self.df.iloc[:, 2].value_counts()
        certificazioni_list = certificazioni_series.index.map(lambda x: str(x).strip()).tolist()
        return certificazioni_list

    

def main():
    print("Prova della classe Accredia:")
    prova = Accredia("20200203_accredia.csv")
    print(prova.df.head())
    
if __name__ == '__main__':
    main()