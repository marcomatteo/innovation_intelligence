from data_provider import DataProvider
from file_parser import ParserCsv

class Accredia(DataProvider):

    def __init__(self):
        self.file_path = self.root_path + r"Accredia/"
        self.file_parser = ParserCsv(self.file_path + "Accredia2020.csv")
        self.df = self.file_parser.open_file(sep="|")
        self.column_types = {
            0: 'object',
            1: 'object',
            2: 'object',
            3: 'int',
            4: 'object'
        }