import os
import pandas as pd
from file_parser import IParser

class ParserCsv(IParser):

    def __init__(self, file_path: str, sep=None):
        self.file_path = file_path

        if not self.file_ext == "csv": 
            raise ValueError("Wrong file extension!")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Path {file_path} error. File not found!")
        
    def open_file(self, sep: str = ',', 
                  *args, **kwargs) -> pd.DataFrame:
        """
        Open a csv file. 
        Returns a pandas.DataFrame
        """
        return pd.read_csv(
                self.file_path, 
                sep = sep,
                dtype = object, 
                keep_default_na = False, 
                na_values = "",
                *args, **kwargs
            )
            
if __name__ == '__main__':
    print("IParserCsv.py")
    file_path = r"/data/data_tests/IParsers/test_file.csv"
    parser = ParserCsv(file_path)