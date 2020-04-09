import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)

import pandas as pd
import os
from file_parser import IParser

class ParserXls(IParser):

    def __init__(self, file_name: str):
        file_ext = self.get_file_ext(file_name)
        if not file_ext.startswith("xls"): 
            raise ValueError("Invalid extension {}".format(file_ext))
        if not os.path.isfile(file_name):
            raise FileNotFoundError("File {} not found!".format(file_name))

        self.file_name = file_name
        
    def open_file(self, *args, **kwargs) -> pd.DataFrame:
        """
        Open a xls file. 
        Returns a pandas.DataFrame
        """
        return pd.read_excel(
                self.file_name, 
                dtype = object, 
                keep_default_na = False, 
                na_values = "",
                engine="openpyxl",
                *args, **kwargs
            )

if __name__ == '__main__':
    print("IParserXls.py")
    file_path = r"/data/data_tests/IParsers/test_file.xlsx"
    parser = ParserXls(ROOT + file_path)