import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence/"
if ROOT not in sys.path:
    sys.path.append(ROOT)

import abc
import numpy as np
import pandas as pd
from collections import defaultdict

class DataProviderMeta(type):
    def __call__(cls, *args, **kwargs):
        class_object = type.__call__(cls, *args, **kwargs)
        class_object.check_required_attributes()
        return class_object

class DataProvider(metaclass = abc.ABCMeta):

    # root_path = ROOT + r"data/"
    root_path = r"/mnt/c/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence/data/"
    file_path = NotImplemented      # type: str
    file_parser = NotImplemented    # type: IParser
    df = NotImplemented             # type: pandas.DataFrame
    column_types = NotImplemented  # type: defaultdict(str)

    def check_required_attributes(self):
        if self.file_path is NotImplemented:
            raise NotImplementedError("Subclass must define self.file_path attribute. \n"\
                + "This attribute should define the DataProvider directory for files to parse.")
        
        if self.file_parser is NotImplemented:
            raise NotImplementedError("Subclass must define self.file_parser attribute. \n"\
                + "This attribute should define the DataProvider file parser.")

        if self.df is NotImplemented:
            raise NotImplementedError("Subclass must define self.df attribute. \n"\
                + "This attribute should define the DataProvider pandas.DataFrame.")

        if self.column_types is NotImplemented:
            raise NotImplementedError("Subclass must define self.column_types attribute. \n"\
                + "This attribute should define the DataProvider column types for the certificate class.")

    def get_column_names(self) -> list:
        if not self.df is NotImplemented:
            return self.df.columns.tolist()

    def get_casted_dataframe(self) -> pd.DataFrame:
        if ((not self.df is NotImplemented) and
            (not self.column_types is NotImplemented)):
            columns_casted = defaultdict(pd.DataFrame)
            for num, _ in enumerate(self.df.columns):
                columns_casted[num] = DataProvider.get_casted_column_for_type(
                    self.df.iloc[:, num], self.column_types[num]
                )
            return pd.concat(columns_casted, axis=1)
    
    def get_column_types(self) -> list:
        if ((not self.df is NotImplemented) and
            (not self.column_types is NotImplemented)):
            return self.get_casted_dataframe().dtypes.tolist()
    
    @staticmethod
    def get_casted_column_for_type(s: pd.Series, col_type: str) -> pd.DataFrame:
        df = s.to_frame()
        if col_type == "int":
            try:
                df_casted = df.fillna(0).astype('int64')
            except:
                df_casted = df
        elif col_type == "float":
            try:
                df_casted = df.astype('float64')
            except:
                df_casted = df
        elif col_type == "object":
            try:
                df_casted = df.astype('object')
            except:
                df_casted = df
        
        return df_casted