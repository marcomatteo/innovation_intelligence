import pandas as pd
import numpy as np
import os

from .dataProvider import DataProvider
from .dataProviderUtil import formatFiscalcodeColumn 
from file_parser import ParserXls

class AtecoInfocamere(DataProvider):
    source_type = "Infocamere"
   
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_path = self.file_path + r"Infocamere/Datasets/" + self.file_name
        self.sheet_name = "FRIULI codici attività"
        try:
            self.open_source()
        except TypeError:
            print("The file type is not xls or xlsx.")
        except FileExistsError:
            print("Check the file_name path.")
        #self.df = self.get_SedeUl_column()

    def get_SedeUl_column(self):
        def addUL(x):
            """
            Funzione che aggiunge la colonna SedeUL
            al file fonte di AtecoInfocamere perché
            solo presente con colonna 'loc'.

            Aggiunge SEDE al posto di 0
            altrimenti UL- + num se num != 0
            """
            if x == 0:   
                return "SEDE"
            return "UL-" + str(x)

        return self.df.assign(
                SedeUl = lambda df: df["loc"].map(lambda x: addUL(x))
            )

    def open_source(self):
        """
        Open the sheet 0 in the Infocamere excel file
        """  
        assert self.file_ext.startswith("xls"), TypeError("Wrong file extension!")
        assert os.path.isfile(self.file_path), FileExistsError("File not found!")

        self.df = ParserXls(self.file_path).open_file(sheet_name=self.sheet_name)

def main():
    print("Prova della classe Anagrafica di Infocamere:")
    try:
        ateco = AtecoInfocamere("Infocamere_06feb2019bis.xlsx")
    except:
        raise ValueError("Errore! Il file non è stato correttamente aperto.")
    
    print(ateco.file_name)


if __name__ == '__main__':
    main()