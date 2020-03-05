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
        parser_col_types = {
            0: np.dtype('object'), #c fiscale
            1: np.dtype('object'), #PRV - Provincia
            2: np.dtype('object'), #N-REG-IMP - Numero Registro Imprese
            3: np.dtype('object'), #rea
            4: np.dtype('object'), #UL-SEDE - Unità Locale o sede dell'impresa
            5: np.dtype('object'), #N-ALBO-AA - Numero di iscrizione all'Albo Imprese Artigiane
            6: np.dtype('object'), #SEZ-REG-IMP - Sezione di iscrizione dell'impresa al Registro del
            7: np.dtype('object'), #NG - Natura Giuridica
            8: np.dtype('object'), #natura giuridica
            9: np.dtype('object'), #tipo impresa
            10: np.dtype('datetime64[ns]'), #DT-ISCR-RI - Data di iscrizione al Registro Imprese
            11: np.dtype('datetime64[ns]'), #DT-ISCR-RD - Data di iscrizione al Registro delle Ditte
            12: np.dtype('datetime64[ns]'), #DT-ISCR-AA - Data di iscrizione all'Albo delle Imprese Artigiane
            13: np.dtype('datetime64[ns]'), #DT-APER-UL - Data di apertura dell'Unità Locale
            14: np.dtype('datetime64[ns]'), #cancellazione
            15: np.dtype('datetime64[ns]'), #DT-INI-AT - Data di inizio attività dell'impresa
            16: np.dtype('datetime64[ns]'), #dt cessazione attività
            17: np.dtype('datetime64[ns]'), #fallimento
            18: np.dtype('datetime64[ns]'), #DT-LIQUID - Data liquidazione dell'impresa
            19: np.dtype('object'), #DENOMINAZIONE - Denominazione dell'impresa
            20: np.dtype('object'), #INDIRIZZO
            21: np.dtype('object'), #STRAD - Via
            22: np.dtype('object'), #CAP
            23: np.dtype('object'), #COMUNE
            24: np.dtype('object'), #FRAZIONE
            25: np.dtype('object'), #ALTRE-INDICAZIONI - Altre indicazioni relative all'indirizz del
            26: np.dtype('int32'), #AA-ADD - Anno di dichiarazione degli addetti
            27: np.dtype('object'), #IND - Numero addetti indipendenti
            28: np.dtype('int32'), #DIP - Numero addetti dipendenti
            29: np.dtype('object'), #PARTITA IVA
            30: np.dtype('object'), #TELEFONO
            31: np.dtype('float64'), #CAPITALE - Capitale sociale dell'impresa
            32: np.dtype('object'), #ATTIVITA' - Descrizione dell'attività principale dell'impresa
            33: np.dtype('object'), #VALUTA-CAPITALE - Valuta del capitale sociale dell'impresa
            34: np.dtype('object'), #stato impresa/ul
            35: np.dtype('object'), #tipo sede/ul1
            36: np.dtype('object'), #tipo sede/ul2
            37: np.dtype('object'), #tipo sede/ul3
            38: np.dtype('object'), #tipo sede/ul4
            39: np.dtype('object'), #tipo sede/ul5
            40: np.dtype('object'), #Presenza di sedi secondarie all'estero
            41: np.dtype('object'), #Impresa estera con unità locale in Friuli Venezia Giulia
            42: np.dtype('object'), #sezione Impresa - Indicazione delle imprese che sono PMI
            43: np.dtype('object'), #sezione Impresa - Indicazione delle imprese che sono start up
            44: np.dtype('object'), #Impr Femminile
            45: np.dtype('object'), #Impr Giovane
            46: np.dtype('object'), #Impr Straniera
            47: np.dtype('object'), #pec
        }  

        col_types = {
            0: np.dtype('object'), #c fiscale
            29: np.dtype('object'), #PARTITA IVA
        }
         
        if (self.file_ext == 'xls') | (self.file_ext == 'xlsx'):
            if self.sheet_name is not None:
                self.df = pd.read_excel(
                    self.file_name, sheet_name=self.sheet_name, 
                    dtype=col_types)
            else:
                self.df = pd.read_excel(self.file_name)
        #TODO: FARE CASTING PER LE ALTRE COLONNE CHE DEVONO ESSERE OBJECT DOPO APERTURA FILE 

def main():
    print("Prova della classe Anagrafica di Infocamere:")
    try:
        anagrafica = AnagraficaInfocamere("Infocamere_06feb2019bis.xlsx")
    except:
        raise ValueError("Errore! Il file non è stato correttamente aperto.")
    
    print(anagrafica.file_name)


if __name__ == '__main__':
    main()