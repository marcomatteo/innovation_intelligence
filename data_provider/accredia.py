from typing import Union
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

    def filter_fiscalcodes_dataframe(self, inplace) -> Union[None, pd.DataFrame]:
        return super().filter_fiscalcodes_dataframe(0, inplace=inplace)