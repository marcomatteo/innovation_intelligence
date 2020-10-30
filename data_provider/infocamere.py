from data_provider import DataProvider
from file_parser import ParserXls

import logging
import pandas as pd
import numpy as np

# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s %(levelname)-5s %(name)-8s (%(funcName)s) %(message)s",
#     datefmt="%d-%m-%Y %H:%M:%S"
# )

logger = logging.getLogger(__name__)


class Infocamere(DataProvider):

    def __init__(self, inTest=False):
        self.inTest = inTest
        self.file_path = self.root_path + r"Infocamere/"
        self.file_parser = ParserXls(self.file_path + "Infocamere.xlsx")


class AnagraficaInfocamere(Infocamere):

    def __init__(self, inTest=False):
        super().__init__(inTest=inTest)
        self.sheet_name = 0
        
        self.column_types = {
            0: "object",
            1: "object",
            2: "object",
            3: "object",
            4: "object",
            5: "object",
            6: "object",
            7: "object",
            8: "object",
            9: "object",
            10: "date",
            11: "date",
            12: "date",
            13: "date",
            14: "date",
            15: "date",
            16: "date",
            17: "date",
            18: "date",
            19: "object",
            20: "object",
            21: "object",
            22: "object",
            23: "object",
            24: "object",
            25: "object",
            26: "int",
            27: "object",
            28: "int",
            29: "object",
            30: "object",
            31: "float",
            32: "object",
            33: "object",
            34: "object",
            35: "object",
            36: "object",
            37: "object",
            38: "object",
            39: "object",
            40: "object",
            41: "object",
            42: "object",
            43: "object",
            44: "object",
            45: "object",
            46: "object",
            47: "object",
            48: "object",
        }

        self.column_constraints = {i: False for i in range(48)}
        self.column_constraints[0] = True
        self.column_constraints[1] = True
        self.column_constraints[4] = True
        
        self.df = self.file_parser.open_file(sheet_name=self.sheet_name)

    def check_file_is_preprocessed(self, cess_artigiana_col: str) -> bool:
        """
        Metodo per controllare se il file necessita di una pre-elaborazione.
        La pre-elaborazione consiste nel controllare la presenza della colonna
        'Cessazione artigiana'. 
        """

        if (cess_artigiana_col != 'pec') | (cess_artigiana_col in self.df.columns):
            logger.debug("Pre-elaborazione file di Infocamere...")
            self.preprocessing_anagrafica(cess_artigiana_column=cess_artigiana_col)
            self.save_new_anagrafica_into_file()

            return False
        else:
            return True

    def preprocessing_anagrafica(self, cess_artigiana_column):
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
        """
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
        logger.debug("Elaborazione colonne {}".format(
            [cess_artigiana_column] + working_columns))
        logger.debug("Elementi dalla colonna '{}' da modificare: {}".format(
            cess_artigiana_column, self.df[cess_artigiana_filter].shape[0]))
        logger.debug("Elementi dalla colonna '{}' da modificare: {}".format(
            working_columns[0], self.df[first_column_to_update_filter].shape[0]))
        logger.debug("Elementi dalla colonna '{}' da modificare: {}".format(
            working_columns[1], self.df[second_column_to_update_filter].shape[0]))

        return cess_artigiana_filter

    def clean_column_cess_artigiana(self, cess_artigiana_column: str):
        """
        Metodo per rimuovere la colonna 'Cessazione artigiana'

        Arguments:
            cess_artigiana_column {str} --- nome della colonna da rimuovere
        """
        logger.debug("Eliminazione della colonna {}".format(
            cess_artigiana_column))
        self.df.drop(columns=cess_artigiana_column, inplace=True)
        logger.debug("Colonna {} eliminata".format(cess_artigiana_column))

    def save_new_anagrafica_into_file(self):
        """
        Metodo per salvare il nuovo file anagrafica aggiornato in un nuovo
        foglio del file fonte
        """
        new_sheet = "nFRIULI Anagrafica"
        logger.debug(
            "Salvataggio dell'anagrafica aggiornata nel foglio '{}'".format(new_sheet))

        self.file_parser.write_new_sheet_into_file(
            self.df, sheet_name=new_sheet, datetime_format="DD/MM/YYYY")


class BilanciInfocamere(Infocamere):

    def __init__(self, inTest=False):
        super().__init__(inTest=inTest)
        self.sheet_name = 1
        self.df = self.file_parser.open_file(sheet_name=self.sheet_name)
        self.column_types = {
            0: 'object',
            1: 'object',
            2: 'object',
            3: 'int',
            4: 'float',
            5: 'float',
            6: 'float',
            7: 'float',
            8: 'float',
            9: 'float',
            10: 'float',
            11: 'float',
            12: 'float',
            13: 'float',
            14: 'float',
            15: 'float'
        }
        self.column_constraints = {i: False for i in range(16)}
        self.column_constraints[0] = True
        self.column_constraints[1] = True
        self.column_constraints[3] = True


class AtecoInfocamere(Infocamere):

    def __init__(self, inTest=False):
        super().__init__(inTest=inTest)
        self.sheet_name = 2
        self.df = self.file_parser.open_file(sheet_name=self.sheet_name)
        self.column_types = {
            0: "object",
            1: "object",
            2: "object",
            3: "int",
            4: "object",
            5: "object",
            6: "object"
        }
