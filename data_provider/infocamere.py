from data_provider import DataProvider
from file_parser import ParserXls

class Infocamere(DataProvider):

    def __init__(self):
        self.file_path = self.root_path + r"Infocamere/"
        self.file_parser = ParserXls(self.file_path + "Infocamere2020.xlsx")

class AnagraficaInfocamere(Infocamere):

    def __init__(self):
        super().__init__()
        self.df = self.file_parser.open_file(sheet_name=0)
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
            18: "object",        
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
        # self.column_constraints

class BilanciInfocamere(Infocamere):

    def __init__(self):
        super().__init__()
        self.df = self.file_parser.open_file(sheet_name=1)
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
        # self.column_constraints


class AtecoInfocamere(Infocamere):

    def __init__(self):
        super().__init__()
        self.df = self.file_parser.open_file(sheet_name=2)
        self.column_types = {
            0: "object",        
            1: "object",
            2: "object",
            3: "int",
            4: "object",
            5: "object",
            6: "object"
        }