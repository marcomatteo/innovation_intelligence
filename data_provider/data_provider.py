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
    file_path = NotImplemented          # type: str
    file_parser = NotImplemented        # type: IParser
    df = NotImplemented                 # type: pandas.DataFrame
    column_types = NotImplemented       # type: defaultdict(str)
    column_constraints = NotImplemented # type: defaultdict(bool)

    @staticmethod
    def get_casted_column_for_type(s: pd.Series, col_type: str) -> pd.DataFrame:
        df = s.to_frame()
        df_casted = None
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

    @staticmethod
    def get_column_max_length_is_respected(s: pd.Series) -> int:
        
        def get_trimmed_length(x) -> int:
            try:
                cond = np.isnan(x)
            except TypeError:
                cond = False # No Not a number

            if cond:
                return 0
            
            s = str(x).strip()
            return len(s)
        
        length = s.map(lambda values: get_trimmed_length(values))
        return length.max(axis=0)

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
        
        if self.column_constraints is NotImplemented:
            raise NotImplementedError("Subclass must define self.column_constraints attribute. \n"\
                + "This attribute should define the DataProvider column constraints for the certificate class.")
        
    def get_column_names(self) -> list:
        """
        Metodo che ritorna il nome delle colonne del Data Provider
        """
        if not self.df is NotImplemented:
            return self.df.columns.tolist()

    def get_casted_dataframe(self) -> pd.DataFrame:
        """
        Metodo che effettua la conversione del file fonte
        secondo indicazione delle colonne per il Data Provider specifico
        """
        if ((not self.df is NotImplemented) and
            (not self.column_types is NotImplemented)):
            columns_casted = defaultdict(pd.DataFrame)
            for num, col_type in self.column_types.items():
                columns_casted[num] = DataProvider.get_casted_column_for_type(
                    self.df.iloc[:, num], col_type
                )
            return pd.concat(columns_casted, axis=1)
    
    def get_column_types(self) -> list:
        """
        Metodo che ritorna la tipologia delle colonne convertite
        da self.get_casted_dataframe()
        """
        if ((not self.df is NotImplemented) and
            (not self.column_types is NotImplemented)):
            return self.get_casted_dataframe().dtypes.tolist()

    def get_columns_max_length(self) -> dict:
        """
        Metodo che ritorna la lunghezza massima nelle colonne di un pd.DataFrame
        """    
        column_is_max_length_respected_dict = defaultdict(bool)
        for num, _ in enumerate(self.df.columns):
            column_is_max_length_respected_dict[num] = DataProvider \
                .get_column_max_length_is_respected(
                    self.df.iloc[:, num]
                )

        return column_is_max_length_respected_dict

    def get_column_nullables(self) -> dict:
        """
        Metodo che ritorna True se presenti dei valori mancanti
        False altrimenti 
        """
        def get_column_nullable(s: pd.Series) -> bool:
            return s.isna().any()

        column_is_nullable = defaultdict(bool)
        for num, _ in enumerate(self.df.columns):
            column_is_nullable[num] = get_column_nullable(
                    self.df.iloc[:, num]
                )

        return column_is_nullable

    def get_column_constraints_is_respected(self) -> int:
        """
        Metodo che ritorna il numero di duplicati (se presenti)
        """
        columns = [
            col for i, col in enumerate(self.get_column_names())
            if self.column_constraints[i] ]
            
        return self.df.duplicated(subset = columns).sum() #.shape[0]