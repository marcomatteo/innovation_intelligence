import pandas as pd
import numpy as np

from .dataProvider import DataProvider
from .dataProviderUtil import formatFiscalcodeColumn 

class AnagraficaInfocamere(DataProvider):
    source_type = "Infocamere"
   
    def __init__(self, file_name):
        self.file_name = self.file_path + r"Infocamere/" + file_name
        self.sheet_name = 0
        self.open_source()

    def open_source(self):
        """
        Method that override the superclass method.
        # TODO: rewrite the classes in SOLID
        """
        if (self.file_ext == 'xls') | (self.file_ext == 'xlsx'):
            if self.sheet_name is not None:
                self.df = pd.read_excel(self.file_name, sheet_name=self.sheet_name)
            else:
                self.df = pd.read_excel(self.file_name)

def main():
    print("Prova della classe Anagrafica di Infocamere:")
    try:
        anagrafica = AnagraficaInfocamere("Infocamere_06feb2019bis.xlsx")
    except:
        raise ValueError("Errore! Il file non è stato correttamente aperto.")
    
    print(anagrafica.file_name)


if __name__ == '__main__':
    main()