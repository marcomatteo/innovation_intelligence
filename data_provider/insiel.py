from functools import partial
from data_provider import DataProvider
from file_parser import ParserXls
from utilities import create_logger
from pathlib import Path
import pandas as pd
import numpy as np

class Insiel(DataProvider):

    def __init__(self, inTest=False):
        self.inTest = inTest
        self.file_path = self.root_path + r"Insiel/"
        self.file_parser = ParserXls(self.file_path + "Insiel.xlsx")


class AnagraficaInsiel(Insiel):

    def __init__(self, inTest=False):
        super().__init__(inTest=inTest)
        self.sheet_name = 0
        
        names = [
            "c fiscale",                                                                
            "PRV - Provincia",                                                          
            "N-REG-IMP - Numero Registro Imprese",                                      
            "rea",                                                                      
            "UL-SEDE - Unità Locale o sede dell'impresa",                              
            "N-ALBO-AA - Numero di iscrizione all'Albo Imprese Artigiane",              
            "SEZ-REG-IMP - Sezione di iscrizione dell'impresa al Registro del",         
            "NG - Natura Giuridica",                                                    
            "natura giuridica",                                                         
            "tipo impresa",                                                             
            "DT-ISCR-RI - Data di iscrizione al Registro Imprese",               
            "DT-ISCR-RD - Data di iscrizione al Registro delle Ditte",           
            "DT-ISCR-AA - Data di iscrizione all'Albo delle Imprese Artigiane",  
            "DT-APER-UL - Data di apertura dell'Unità Locale",                   
            "cancellazione",                                                            
            "DT-INI-AT - Data di inizio attività dell'impresa",                  
            "dt cessazione attività",                                                   
            "fallimento",                                                        
            "DT-LIQUID - Data liquidazione dell'impresa",                        
            "DENOMINAZIONE - Denominazione dell'impresa",                        
            "INDIRIZZO",                                                         
            "STRAD - Via",                                                       
            "CAP",                                                               
            "COMUNE",                                                            
            "FRAZIONE",                                                          
            "ALTRE-INDICAZIONI - Altre indicazioni relative all'indirizz del",   
            "AA-ADD - Anno di dichiarazione degli addetti",                      
            "IND - Numero addetti indipendenti",                                 
            "DIP - Numero addetti dipendenti",                                   
            "PARTITA IVA",                                                       
            "TELEFONO",                                                          
            "CAPITALE - Capitale sociale dell'impresa",                          
            "ATTIVITA' - Descrizione dell'attività principale dell'impresa",     
            "VALUTA-CAPITALE - Valuta del capitale sociale dell'impresa",        
            "stato impresa/ul",                                                  
            "tipo sede/ul1",                                                     
            "tipo sede/ul2",                                                     
            "tipo sede/ul3",                                                     
            "tipo sede/ul4",                                                     
            "tipo sede/ul5",                                                     
            "Presenza di sedi secondarie all'estero",                            
            "Impresa estera con unità locale in Friuli Venezia Giulia",          
            "sezione Impresa - Indicazione delle imprese che sono PMI",          
            "sezione Impresa - Indicazione delle imprese che sono start up",     
            "Impr Femminile",                                                    
            "Impr Giovane",                                                      
            "Impr Straniera",                                                    
            "pec",                                                               
            "Cessazione artigiana",                                              
            "DT-COST - Data costituzione",
            "Tipo Localizzazione"
            ]             

        open_file = partial(
            self.file_parser.open_file, 
            sheet_name=self.sheet_name, names=names, skiprows=2)
        
        try:
            self.df = open_file()
        except:
            _ = names.pop(-3)
            self.df = open_file()

        print("\nAperto il file di Insiel")

        if not self.is_preprocessed("Cessazione artigiana"):
            print("\nAttenzione: File non elaborato, bisogna aggiornare le date " + \
                    "di iscrizione all'albo imprese artigiane.\n" + \
                    "Utilizzare il metodo update_artisan()\n")


    def is_preprocessed(self, cess_artigiana_col: str) -> bool:
        """
        Metodo per controllare se il file necessita di una pre-elaborazione. 
        """
        if (cess_artigiana_col in self.df.columns):
            return False
        else:
            return True

    def update_artisan(self, cess_artigiana_col: str, log_path=None, save:bool=True):
        if log_path:
            if isinstance(log_path, str):
                log_path = Path(log_path)
            elif not isinstance(log_path, Path):
                raise ValueError("Path must be a pathlib.Path istance")

        self.logger = create_logger("InsielPreprocessing", path=log_path, verbose=True)

        self.preprocessing_anagrafica(cess_artigiana_column=cess_artigiana_col)
        if save:
            self.save_new_anagrafica_into_file()

    def preprocessing_anagrafica(self, cess_artigiana_column):
        """
        Metodo che permette di preparare il file di Insiel
        per poterlo inserire all'interno di Innovation Intelligence.

        Campi aggiornati:
        -----------------

            - "N-ALBO-AA - Numero di iscrizione all'Albo Imprese Artigiane"

            - "DT-ISCR-AA - Data di iscrizione all'Albo delle Imprese Artigiane"

        Campi eliminati:
        ----------------

            - "Cessazione artigiana"
        """
        self.logger.debug("Pre-elaborazione file di Insiel...")
        working_columns = [
            "N-ALBO-AA - Numero di iscrizione all'Albo Imprese Artigiane",
            "DT-ISCR-AA - Data di iscrizione all'Albo delle Imprese Artigiane"
        ]

        # Setup
        cess_artigiana_filter = self.get_cessazione_artigiana_filter(
            cess_artigiana_column, working_columns)

        # Preprocessing
        self.df.loc[cess_artigiana_filter, working_columns] = np.nan

        # Cleaning
        self.clean_column_cess_artigiana(cess_artigiana_column)

    def get_cessazione_artigiana_filter(self,
                                        cess_artigiana_column: str, working_columns: list) -> pd.Series:
        """
        Metodo per rendicontare il numero di elementi che la pre-elaborazione
        andrà a modificare

        Arguments:
        ----------
        working_columns {list} 
        Colonne da modificare

        cess_artigiana_filter {pd.Series} 
        Serie bool per identificare le righe da aggiornare
        """
        cess_artigiana_filter = self.df[cess_artigiana_column].notna()
        first_column_notna_filter = self.df[working_columns[0]].notna()
        second_column_notna_filter = self.df[working_columns[1]].notna()

        first_column_to_update_filter = first_column_notna_filter & cess_artigiana_filter
        second_column_to_update_filter = second_column_notna_filter & cess_artigiana_filter

        # Logs
        self.logger.debug("Elaborazione colonne {}".format(
            [cess_artigiana_column] + working_columns))
        self.logger.debug("Elementi dalla colonna '{}' da modificare: {}".format(
            cess_artigiana_column, self.df[cess_artigiana_filter].shape[0]))
        self.logger.debug("Elementi dalla colonna '{}' da modificare: {}".format(
            working_columns[0], self.df[first_column_to_update_filter].shape[0]))
        self.logger.debug("Elementi dalla colonna '{}' da modificare: {}".format(
            working_columns[1], self.df[second_column_to_update_filter].shape[0]))

        return cess_artigiana_filter

    def clean_column_cess_artigiana(self, cess_artigiana_column: str):
        """
        Metodo per rimuovere la colonna 'Cessazione artigiana'

        Arguments:
            cess_artigiana_column {str} --- nome della colonna da rimuovere
        """
        self.logger.debug("Eliminazione della colonna {}".format(
            cess_artigiana_column))
        self.df.drop(columns=cess_artigiana_column, inplace=True)
        self.logger.debug("Colonna {} eliminata".format(cess_artigiana_column))

    def save_new_anagrafica_into_file(self):
        """
        Metodo per salvare il nuovo file anagrafica aggiornato in un nuovo
        foglio del file fonte
        """
        new_sheet = "nFRIULI Anagrafica"
        self.logger.debug(
            "Salvataggio dell'anagrafica aggiornata nel foglio '{}'".format(new_sheet))

        self.file_parser.write_new_sheet_into_file(
            self.df, sheet_name=new_sheet, datetime_format="DD/MM/YYYY")
        
        self.logger.debug("Salvataggio completato")


class BilanciInsiel(Insiel):

    def __init__(self, inTest=False):
        super().__init__(inTest=inTest)
        self.sheet_name = 1
        self.df = self.file_parser.open_file(sheet_name=self.sheet_name)

    def drop_bs(self, year: int):
        """
        Drop the balance sheets with "Anno" == year

        Args:
            year (int): anno di bilancio da eliminare
        """
        cond = self.df.anno.isin([year for year in range(2010, year)])
        self.df = self.df.loc[cond]
        self.file_parser.write_new_sheet_into_file(
            self.df, 
            sheet_name=f"FRIULI dati storicizzati-{year}", 
            datetime_format="DD/MM/YYYY")
        return self.df


class AtecoInsiel(Insiel):

    def __init__(self, inTest=False):
        super().__init__(inTest=inTest)
        self.sheet_name = 1

        if self.is_preprocessed():
            self.df = self.file_parser.open_file(sheet_name=self.sheet_name)
        else:
            self.df = self.file_parser.open_file(
                sheet_name=self.sheet_name, skiprows=2)

    def is_preprocessed(self) -> bool:
        tmp_df = self.file_parser.open_file(
            sheet_name=self.sheet_name, skiprows=2, nrows=100)

        return False if 'c fiscale' in tmp_df.columns else True

    def clean_nan(self, inplace:bool=False):
        return self.df.dropna(axis=0, how='any', inplace=inplace)

    def save_new_sheet(self):
        """
        Metodo per salvare il nuovo file ateco aggiornato in un nuovo
        foglio del file fonte
        """
        new_sheet = "nFRIULI codici attivita"

        self.file_parser.write_new_sheet_into_file(
            self.df, sheet_name=new_sheet, datetime_format="DD/MM/YYYY")
                          