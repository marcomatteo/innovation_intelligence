import pandas as pd
import numpy as np

from .dataProvider import DataProvider
from .dataProviderUtil import formatFiscalcodeColumn 

class AnagraficaInfocamere(DataProvider):
    source_type = "Infocamere"
   
    def __init__(self, file_name):
        self.file_name = self.file_path + "Infocamere/" + file_name
        self.sheet_name = 'FRIULI anagrafica'
        super().__init__(self.file_name, sheet_name=self.sheet_name)

def main():
    print("Prova della classe Anagrafica di Infocamere:")
    try:
        anagrafica = AnagraficaInfocamere("Infocamere_06feb2019bis.xlsx")
    except:
        raise ValueError("Errore! Il file non è stato correttamente aperto.")
    
    print(anagrafica.file_name)


if __name__ == '__main__':
    main()