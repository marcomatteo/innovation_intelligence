from data_provider import DataProvider
from file_parser import ParserCsv

import pandas as pd

class Accredia(DataProvider):

    def __init__(self, inTest = False):
        self.inTest = inTest
        self.file_parser_sep = "|"
        self.file_path = self.root_path + r"Accredia/"
        self.file_parser = ParserCsv(self.file_path + "Accredia2020.csv")
        self.df = self.file_parser.open_file(sep = self.file_parser_sep)
        self.column_types = {
            0: 'object',
            1: 'object',
            2: 'object',
            3: 'int',
            4: 'object'
        }
        self.column_constraints = {
            0: True,
            1: False,
            2: True,
            3: False,
            4: True
        }

    def get_filtred_fiscal_codes_dataframe(self, cf_list: list) -> pd.DataFrame:
        """Metodo che ritorna una copia del dataframe
        solo per i codici fiscali passati in cf_list"""
        return super().get_filtred_fiscal_codes_dataframe(0, cf_list)
    
    def set_filtred_fiscal_codes_dataframe(self, cf_list: list):
        """Metodo che filtra le righe del dataframe
        solo per i codici fiscali passati in cf_list"""
        super().set_filtred_fiscal_codes_dataframe(0, cf_list)