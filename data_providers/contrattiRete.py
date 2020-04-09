"""
File contenente la classe ContrattiRete per il data provider 
dei "Contratti di rete" in Innovation Intelligence
"""
import pandas as pd
import numpy as np

from data_providers import DataProvider
from file_parser import ParserXls

class ContrattiRete(DataProvider):

    def __init__(self, file_name):
        self.file_name = file_name
        self.file_path = self.file_path + r"Contratti rete/" + self.file_name
       
        self.parser = ParserXls(self.file_path)
        self.elenco = self.parser.open_file(sheet_name="Elenco")
        print("Aperto foglio 'elenco' in ContrattiRete.elenco")
        self.sogg_giuridico = self.parser.open_file(sheet_name="Sogg. Giu.")
        print("Aperto foglio 'Sogg. Giu.' in ContrattiRete.sogg_giuridico")

    def preprocessing_merge_sheets(self) -> pd.DataFrame:
        """
        Preprocessing file fonte Contratti di rete
        """
        # Apertura DF
        file_foglio1 = self.elenco.astype({'progr.' : np.int64})
        file_foglio2 = self.sogg_giuridico.astype({'progr.' : np.int64})
        
        # Sistemazione numero progressivo
        file_foglio2.loc[:,'progr.'] = file_foglio2['progr.'] + file_foglio1['progr.'].max()

        # Aggiunta colonna: Soggetto Giuridico SI/NO
        file_foglio1 = file_foglio1.assign(SoggettoGiuridico = pd.Series(['NO' for i in file_foglio1.index.tolist()]))
        file_foglio2 = file_foglio2.assign(SoggettoGiuridico = pd.Series(['SI' for i in file_foglio1.index.tolist()]))

        # Elenco delle colonne in lista per entrambi i file
        elenco_cols1 = file_foglio1.columns.tolist()
        elenco_cols2 = file_foglio2.columns.tolist()
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

        return file_foglio1.append(file_temp, ignore_index=True, sort=False)
    
def main():
    print("Prova della classe ContrattiRete:")
    try:
        prova = ContrattiRete("Source_ContrattiRete_15052019_updated_manually.xlsx")
        print("Classe ContrattiRete: OK!")
    except:
        print("Non è andata a buon fine.")

    del prova

if __name__ == '__main__':
    main()