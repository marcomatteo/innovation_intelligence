# File contenente la classe ContrattiRete per il data provider dei "Contratti di rete" in Innovation Intelligence

import pandas as pd
import numpy as nps
from data_providers import DataProvider
from innovation_intelligence.db_interface.i2fvg import I2FVG
from sqlalchemy import create_engine

class ContrattiRete(DataProvider):

    def __init__(self, fonte_name):
        # Sistemo il percorso per recuperare il file utilizzando la classe dataProvider e aggiungendo il nome passato dall'inizializzatore
        super().__init__()
        self.fonte_source = self.fonte_source + "Contratti rete\\" + fonte_name
        self.i2fvg_df = self.open_i2fvg()
        # Controllo che tipologia di file fonte si intende aprire
        check = len(fonte_name.split("_"))
        if check == 3:
            # Apertura dei due fogli, merge e pulizia dei duplicati
            pass
        elif check == 4:
            # Apertura con la pulizia dei duplicati
            pass
        elif check == 5:
            # Apertura file aggiornato
            self._lastFileFonte()

    # Apertura del file fonte aggiornato
    def _lastFileFonte(self):
        foglio1 = "Elenco"
        self.fonte_df = pd.read_excel(self.fonte_source, sheet_name=foglio1)
        print("File fonte sui Contratti di Rete importato correttatmente.")

    # Unisco i due fogli del file fonte
    def _mergeFileFonte(self):
        # Nome dei fogli del file excel
        foglio1 = "Elenco"
        foglio2 = "Sogg. Giu."

        # Apertura DF
        file_foglio1 = pd.read_excel(self.fonte_source, sheet_name=foglio1)
        file_foglio2 = pd.read_excel(self.fonte_source, sheet_name=foglio2)

        # Sistemazione dei due DF per la provincia di Napoli
        file_foglio1['PV'].fillna('NA', inplace=True)
        file_foglio2['PV impresa'].fillna('NA', inplace=True)

        # Sistemazione numero progressivo
        file_foglio2.loc[:,['progr.']] = file_foglio2['progr.'] + file_foglio1['progr.'].max()

        # Aggiunta colonna: Soggetto Giuridico SI/NO
        file_foglio1 = file_foglio1.assign(SoggettoGiuridico = pd.Series(['NO' for i in file_foglio1.index.get_values().tolist()]))
        file_foglio2 = file_foglio2.assign(SoggettoGiuridico = pd.Series(['SI' for i in file_foglio1.index.get_values().tolist()]))

        # Elenco delle colonne in lista per entrambi i file
        elenco_cols1 = file_foglio1.columns.get_values().tolist()
        elenco_cols2 = file_foglio2.columns.get_values().tolist()
        cols = { col: col[0] for col in elenco_cols2 }

        # Match chiave e valori del dizionario per rinominare le colonne
        cols[elenco_cols2[0]] = elenco_cols1[0]
        cols[elenco_cols2[1]] = elenco_cols1[1] 
        cols[elenco_cols2[4]] = elenco_cols1[2]
        cols[elenco_cols2[9]] = elenco_cols1[3]
        cols[elenco_cols2[10]] = elenco_cols1[5]
        cols[elenco_cols2[12]] = elenco_cols1[6]
        cols[elenco_cols2[13]] = elenco_cols1[7]
        cols[elenco_cols2[14]] = elenco_cols1[8]
        cols[elenco_cols2[15]] = elenco_cols1[10]
        cols[elenco_cols2[16]] = elenco_cols1[11]
        cols[elenco_cols2[17]] = elenco_cols1[12]
        cols[elenco_cols2[18]] = elenco_cols1[13]
        cols[elenco_cols2[19]] = elenco_cols1[14]
        cols[elenco_cols2[20]] = elenco_cols1[18]

        # Rinomino secondo DF con le colonne del primo
        file_foglio2.rename(columns=cols, inplace=True)
        # Seleziono le colonne che utilizzo e salvo nel DF temp
        file_temp = file_foglio2.loc[:, [v for k, v in cols.items() if len(v)>1]]

        self.fonte_df = file_foglio1.append(file_temp, ignore_index=True, sort=False)
        # Libero memoria non utilizzata
        del file_temp, file_foglio1, file_foglio2
    
    # Apertura tabella di Innovation intelligence
    def open_i2fvg(self):
        name = "DATA_ContrattiRete"
        df = pd.read_sql_table(name, I2FVG.connessione)
        print("Tabella da I2FVG sui Contratti di Rete importata correttamente.")
        return df

    def split_contratti_i2fvg(self, df):
        """
        Metodo costruito per tener traccia della funzione split
        per evidenziare tutte le imprese che hanno partecipato ad un contratto.
        """
        return df.join(
            df['AziendePartecipanti'].str.split(", ", expand=True).head(),
            how='inner'
        )

print("Prova della classe ContrattiRete:")
try:
    prova = ContrattiRete("Source_ContrattiRete_15052019_updated_manually.xlsx")
    print("Classe ContrattiRete: OK!")
except:
    print("Non è andata a buon fine.")

del prova