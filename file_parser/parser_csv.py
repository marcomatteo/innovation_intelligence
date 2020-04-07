import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)

import os
import pandas as pd
from file_parser import IParser

class ParserCsv(IParser):

    def __init__(self, file_name: str, sep=None):
        if not self.get_file_ext(file_name) == "csv": 
            raise ValueError("Wrong file extension!")
        if not os.path.isfile(file_name):
            raise FileNotFoundError("File not found!")
        self.file_name = file_name
        self.sep = sep

    def open_file(self) -> pd.DataFrame:
        """
        Open a csv file. 
        Returns a pandas.DataFrame
        """
        return pd.read_csv(
                self.file_name, 
                sep = self.sep,
                dtype = object, 
                keep_default_na = False, 
                na_values = ""
            )

if __name__ == '__main__':
    print("IParserCsv.py")
    file_path = r"/data/data_tests/IParsers/test_file.csv"
    parser = ParserCsv(ROOT + file_path)