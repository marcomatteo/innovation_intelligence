import pandas as pd
import numpy as np
import os

from .dataProvider import DataProvider
from .dataProviderUtil import formatFiscalcodeColumn 

class AnagraficaInfocamere(DataProvider):
    source_type = "Infocamere"
   
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_path = self.file_path + r"Infocamere/" + self.file_name
        self.sheet_name = 0
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

        self.df = pd.read_excel(self.file_path, sheet_name=0, dtype=object)

        # cols_int32 = [26, 27, 28]
        # cols_float64 = [31]
        # self.df.iloc[:, cols_int32].fillna(0).astype('int32', copy=False)
        # self.df.iloc[:, cols_float64].astype('float64', copy=False)

def main():
    print("Prova della classe Anagrafica di Infocamere:")
    try:
        anagrafica = AnagraficaInfocamere("Infocamere_06feb2019bis.xlsx")
    except:
        raise ValueError("Errore! Il file non è stato correttamente aperto.")
    
    print(anagrafica.file_name)


if __name__ == '__main__':
    main()