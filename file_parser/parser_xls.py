import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)

import pandas as pd
import os
from file_parser import IParser

class ParserXls(IParser):

    def __init__(self, file_path: str):
        self.file_path = file_path
        file_ext = self.file_ext
        if not file_ext.startswith("xls"): 
            raise ValueError("Invalid extension {}".format(file_ext))
        if not os.path.isfile(file_path):
            raise FileNotFoundError("File {} not found!".format(file_path))
        self.excel_file = pd.ExcelFile(self.file_path)

    @property
    def get_sheet_names(self) -> list:
        return self.excel_file.sheet_names

    def open_file(self, *args, **kwargs) -> pd.DataFrame:
        """
        Open a xls file. 
        Returns a pandas.DataFrame
        """
        return pd.read_excel(self.file_path, 
                             dtype = object, 
                             keep_default_na = False, 
                             na_values = "",
                             engine="xlrd",
                             *args, **kwargs)

    def write_new_sheet_into_file(self, df: pd.DataFrame, 
                                  sheet_name = 'NewSheet', 
                                  float_format = "%.2f",
                                  date_format = "DD/MM/YYYY", 
                                  datetime_format = "DD/MM/YY HH:MM:SS",
                                  *args, **kwargs):
        """
        Write into the existing xls file a new sheet
        
        Arguments:
            df {pd.DataFrame} -- Dataframe to save
            sheet_name {str} -- Sheet name to be added
        """
        with pd.ExcelWriter(self.file_path, 
                            date_format = date_format, 
                            datetime_format = datetime_format,
                            mode = 'a', engine = "openpyxl",
                            *args, **kwargs) as writer:
            df.to_excel(
                writer,
                sheet_name = sheet_name,
                float_format = float_format,
                index = False
            )