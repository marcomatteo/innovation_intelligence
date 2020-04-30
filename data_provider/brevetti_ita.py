from file_parser import ParserXls
from data_provider import DataProvider

import pandas as pd

class BrevettiIta(DataProvider):
    
    def __init__(self):
        self.file_path = self.root_path + r"UIBM/"
        self.file_parser = ParserXls(self.file_path + "UIBMSourceSample.xlsx")
        last_sheet_to_open = self.file_parser.get_sheet_names[-1]
        self.df = self.file_parser.open_file(sheet_name=last_sheet_to_open)
        self.column_types = {
            0: 'int',
            1: 'object',
            2: 'date',
            3: 'object',
            4: 'object',
            5: 'int',
            6: 'object',
            7: 'object',
            8: 'object',
            9: 'object',
            10: 'object',
            11: 'object',
            12: 'object',
            13: 'object',
            14: 'object',
            15: 'bool'
        }
        self.column_constraints = {
            i: False for i in range(16)
        }