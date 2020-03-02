import pandas as pd
import numpy as np
from datetime import datetime

# Classe da cui ereditano tutte le varie tipologie di data provider
class DataProvider:
    """
    Generic class for different types of data providers.
    """
    
    # Path of the source files
    file_path = "C:/Users/buzzulini/OneDrive - Area Science Park"\
                + "/Attività/Innovation Intelligence/Fonti/"

    def __init__(self, file_name, sep=None, sheet_name=None):
        # File name
        self.file_name = self.file_path + file_name
        # Csv column separator
        self.sep = sep                  # None if it's Excel
        self.sheet_name = sheet_name    # None if it's CSV
        # DataFrame
        self.open_source()

    @property
    def file_ext(self):
        """
        Get file extension
        """
        return self.file_name.split(".")[-1]

    def open_source(self):
        """
        Method that opens the file_name file and returns it
        as a DataFrame.
        """
        # If CSV
        if self.file_ext == 'csv':
            if self.sep is not None:
                self.df = pd.read_csv(self.file_name, sep=self.sep)
            else:
                self.df = pd.read_csv(self.file_name)
        # If EXCEL
        elif self.file_ext == 'xls' | self.file_ext == 'xlsx':
            if self.sheet_name is not None:
                self.df = pd.read_excel(self.file_name, sheet_name=self.sheet_name)
            else:
                self.df = pd.read_excel(self.file_name)
