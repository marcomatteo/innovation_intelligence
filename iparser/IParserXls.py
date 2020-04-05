import sys
root = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if root not in sys.path:
    sys.path.append(root)

import pandas as pd
import os
from iparser import IParser

class IParserXls(IParser):

    def __init__(self):
        pass

    def open_file(self, path: str, file_name: str, sheet_name=None) -> pd.DataFrame:
        file_path = path + file_name

        if not self.get_file_ext(file_name).startswith("xls"): 
            raise ValueError("Wrong file extension!")
        if not os.path.isfile(file_path):
            raise FileNotFoundError("File not found!")

        return pd.read_excel(
                file_path, 
                sheet_name=sheet_name, 
                dtype=object, 
                keep_default_na=False, 
                na_values=""
            )


if __name__ == '__main__':
    print("IParserXls.py")
    parser = IParserXls()