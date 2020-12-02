from collections import defaultdict, namedtuple
from os import dup
from typing import List

import json

import pandas as pd
import numpy as np

from data_provider import DataProvider


class AcceptanceMeta(type):
    def __call__(cls, *args, **kwargs):
        class_object = type.__call__(cls, *args, **kwargs)
        class_object.check_required_attributes()
        return class_object


class AcceptanceBuilder(metaclass=AcceptanceMeta):
    """
    Super classe che implementa tutte le funzioni
    da utilizzare per controllare un file fonte
    da un Data Provider
    """
    # Soluzione alternativa ai dizionari
    Columns = namedtuple('Columns', ['nome', 'tipologia', 'lunghezza', 'nullable', 'pk'])

    dp = NotImplemented                 # type: DataProvider
    dp_file_extension = NotImplemented  # type: str
    column_number = NotImplemented      # type: int
    columns = NotImplemented            # type: List[Columns]
    
    column_types = NotImplemented       # type: list
    column_max_length = NotImplemented  # type: list
    column_nullables = NotImplemented   # type: list


    def __init__(self, dp, dp_file_extension, columns):
        self.dp = dp
        self.dp_file_extension = dp_file_extension
        self.columns = columns

    @staticmethod
    def get_log_list_from_list(elements: list) -> list:
        """
        Method to format list for logging purposes

        Arguments:
            elements {list} -- list to be printed into a logger

        Returns:
            list
        """
        result = [f"{num} : {value}" for num, value in enumerate(elements)]
        result.append("\n")

        return result

    @staticmethod
    def get_log_list_from_dict(elements: dict) -> list:
        """
        Method to format dict for logging purposes

        Arguments:
            elements {dict} -- dict to be printed into a logger

        Returns:
            list
        """
        # result = {i: f"{num} : {value}\n" for i, (num, value) in enumerate(elements.items())}

        # return result
        result = {key: str(value) for key, value in elements.items()}
        return json.dumps(result)

    def check_required_attributes(self):
        if self.dp is NotImplemented:
            raise NotImplementedError("Subclass must define self.dp attribute. \n"
                                      + "This attribute should define the DataProvider obj of the certificate.")
        if self.dp_file_extension is NotImplemented:
            raise NotImplementedError("Subclass must define self.dp_file_extension attribute. \n"
                                      + "This attribute should define the DataProvider obj of the certificate.")
        if self.columns is NotImplemented:
            raise NotImplementedError("Subclass must define self.columns attribute. \n"
                                      + "This attribute should define the DataProvider obj of the certificate.")
        pass

    def check_file_extension(self) -> str:
        if not self.dp is NotImplemented:
            return self.dp.file_parser.file_ext
        pass

    def check_column_number(self) -> int:
        if ((not self.dp is NotImplemented) and
                (not self.columns is NotImplemented)):
            return self.dp.get_column_number()

    def check_column_types(self) -> list:
        """
        Metodo che ritorna la tipologia delle colonne convertite
        da self.get_casted_dataframe()
        """
        if ((not self.dp is NotImplemented) and
                (not self.columns is NotImplemented)):
            # return self.dp.get_column_types()
            return self.get_casted_dataframe().dtypes.tolist()
        pass

    def get_casted_dataframe(self) -> pd.DataFrame:
        """
        Metodo che effettua la conversione del file fonte
        secondo indicazione delle colonne per il Data Provider specifico
        """
        if ((not self.dp is NotImplemented) and
                (not self.columns is NotImplemented)):

            columns_casted_to_concat = defaultdict(pd.DataFrame)
            col_types = [c.tipologia for c in self.columns]
            for num, col_type in enumerate(col_types):

                columns_casted_to_concat[num] = AcceptanceBuilder \
                    .get_casted_column_for_type(self.dp.df.iloc[:, num], col_type)

            return pd.concat(columns_casted_to_concat, axis=1)

    @staticmethod
    def get_casted_column_for_type(s: pd.Series, col_type: str) -> pd.DataFrame:
        df = s.to_frame()
        df_casted = None
        if col_type == np.dtype('int64'):
            try:
                df_casted = df.fillna(0).astype('int64')
            except:
                df_casted = df
        elif col_type == np.dtype('float64'):
            try:
                df_casted = df.astype('float64')
            except:
                df_casted = df
        elif col_type == np.dtype('<M8[ns]'):
            try:
                df_casted = pd.to_datetime(s).to_frame()
            except:
                df_casted = df
        else:
            df_casted = df

        return df_casted

    def check_column_length(self) -> list:
        if ((not self.dp is NotImplemented) and
                (not self.columns is NotImplemented)):
            return self.dp.get_columns_max_length()
        pass

    def check_column_nullables(self) -> list:
        if ((not self.dp is NotImplemented) and
                (not self.columns is NotImplemented)):
            return self.dp.get_column_nullables()
        pass

    def get_duplicates(self) -> pd.Series:
        if ((not self.dp is NotImplemented) and
                (not self.columns is NotImplemented)):
            pk_cols = {col_name: col.pk for col_name, col in zip(self.dp.df.columns, self.columns)}
            duplicated_cols_list = [nome 
                for nome, _ in filter(lambda el: el[1], pk_cols.items())]
            
            if len(duplicated_cols_list) > 0:
                return self.dp.df.duplicated(subset=duplicated_cols_list)
        
            return pd.Series([], dtype='object')
        pass
