from data_provider import DataProvider
from file_parser import ParserCsv

class Modefinance(DataProvider):

    def __init__(self, inTest = False):
        self.inTest = inTest
        self.file_parser_sep = ";"
        self.file_path = self.root_path + r"Modefinance/"
        self.file_parser = ParserCsv(self.file_path + "modefinance_09_04_2020.csv")
        self.df = self.file_parser.open_file(sep=self.file_parser_sep)
        self.column_types = {
            0: 'object',
            1: 'int',
            2: 'date',
            3: 'object'
        }
        self.column_constraints = {
            0: True,
            1: False,
            2: True,
            3: False
        }