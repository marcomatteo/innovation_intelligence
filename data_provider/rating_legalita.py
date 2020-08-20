from typing import Union
from data_provider import DataProvider
from file_parser import ParserXls

import pandas as pd

class RatingLegalita(DataProvider):

    def __init__(self, inTest = False):
        self.inTest = inTest
        self.file_path = self.root_path + r"RatingLegalita/"
        self.file_parser = ParserXls(self.file_path + "27mar2020.xlsx")
        self.df = self.file_parser.open_file(skiprows=1)
        self.column_types = {
            0: 'object',
            1: 'object',
            2: 'object',
            3: 'object',
            4: 'date',
            5: 'object',
            6: 'object',
            7: 'date'
        }
        self.column_constraints = {col: False for col in self.column_types.keys()}

    def filter_fiscalcodes_dataframe(self, inplace=False) -> Union[None, pd.DataFrame]:
        return super().filter_fiscalcodes_dataframe(1, inplace=inplace)
        
    # def get_filtred_fiscal_codes_dataframe(self, cf_list: list) -> pd.DataFrame:
    #     """Metodo che ritorna una copia del dataframe
    #     solo per i codici fiscali passati in cf_list"""
    #     return super().get_filtred_fiscal_codes_dataframe(1, cf_list)

    # def set_filtred_fiscal_codes_dataframe(self, cf_list: list):
    #     """Metodo che filtra le righe del dataframe
    #     solo per i codici fiscali passati in cf_list"""
    #     super().set_filtred_fiscal_codes_dataframe(1, cf_list)

    def update_rating_column_with_spaces(self):
        """Aggiunge uno spazio tra l'asterisco e il rating
        Esempio: '*++' -> '* ++'"""

        values = self.df.iloc[:, -2].str.rsplit("*", n=1)
        self.df.iloc[:, -2] = values.map(lambda l: "* ".join(l) 
                                            if isinstance(l, list) else l)
        
