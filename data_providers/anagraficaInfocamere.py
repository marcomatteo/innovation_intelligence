import pandas as pd
import numpy as np
import os

from .dataProvider import DataProvider
from .dataProviderUtil import formatFiscalcodeColumn 

class AnagraficaInfocamere(DataProvider):
    source_type = "Infocamere"
   
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_path = self.file_path + r"Infocamere/Datasets/" + self.file_name
        self.sheet_name = "FRIULI anagrafica"
        try:
            self.open_source()
        except TypeError:
            print("The file type is not xls or xlsx.")
        except FileExistsError:
            print("Check the file_name path.")

    def open_source(self):
        """
        Open the sheet 0 in the Infocamere excel file
        """  
        assert self.file_ext.startswith("xls"), TypeError("Wrong file extension!")
        assert os.path.isfile(self.file_path), FileExistsError("File not found!")

        self.df = pd.read_excel(
                self.file_path, 
                sheet_name=self.sheet_name, 
                dtype=object, 
                keep_default_na=False, 
                na_values=""
            )

    def preprocessing_anagrafica(self) -> pd.DataFrame:
        """
        Metodo che permette di preparare il file di Infocamere
        per poterlo inserire all'interno di Innovation Intelligence.

        Campi aggiornati:
        -----------------

            - "N-ALBO-AA - Numero di iscrizione all'Albo Imprese Artigiane"

            - "DT-ISCR-AA - Data di iscrizione all'Albo delle Imprese Artigiane"
        
        Campi eliminati:
        ----------------

            - "Cessazione artigiana"

        Return:
        -------

            pd.DataFrame
        """
        print("\nPreprocessing anagrafica: \tElaborazione file fonte Infocamere...\n")
        cess_artigiana_col = "Cessazione artigiana"
        to_change_cols = [
            "N-ALBO-AA - Numero di iscrizione all'Albo Imprese Artigiane",
            "DT-ISCR-AA - Data di iscrizione all'Albo delle Imprese Artigiane"
        ]
        df = self.df.copy()
        print("Info campi originali del file:\n")
        df.loc[:, to_change_cols + [cess_artigiana_col]].info()
        # %% Preprocessing
        if cess_artigiana_col in df.columns:
            cond = df[cess_artigiana_col].notna()
            df.loc[cond, to_change_cols] = np.nan
        print("\n\nPulizia campi impresa Artigiana effettuata...\n")
        print("Info campi modificati del file:\n")
        df.loc[:, to_change_cols + [cess_artigiana_col]].info()
        # %% Drop column cess_artigiana_col
        df.drop(columns=cess_artigiana_col, inplace=True)
        print("\n\nEliminazione colonna {} effettuata...\n".format(cess_artigiana_col))
        print("Preprocessing Anagrafica ultimato.")
        return df


def main():
    print("Prova della classe Anagrafica di Infocamere:")
    try:
        anagrafica = AnagraficaInfocamere("Infocamere_06feb2019bis.xlsx")
    except:
        raise ValueError("Errore! Il file non è stato correttamente aperto.")
    
    print(anagrafica.file_name)


if __name__ == '__main__':
    main()