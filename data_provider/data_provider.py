import abc
from file_parser.iparser import IParser
import numpy as np
import pandas as pd
from collections import defaultdict
from typing import Union


class DataProviderMeta(type):
    def __call__(cls, *args, **kwargs):
        class_object = type.__call__(cls, *args, **kwargs)
        class_object.check_required_attributes()
        return class_object


class DataProvider(metaclass=abc.ABCMeta):

    data_dir = r"data/"

    test_path = data_dir + r"data_tests/"

    inTest = NotImplemented             # type: bool
    file_path = NotImplemented          # type: str
    file_parser = NotImplemented        # type: IParser
    df = NotImplemented                 # type: pd.DataFrame
    column_types = NotImplemented       # type: defaultdict(str)
    column_constraints = NotImplemented  # type: defaultdict(bool)

    def __init__(self, df, column_types, column_constraints):
        self.df = df
        self.column_types = column_types
        self.column_constraints = column_constraints

    @property
    def root_path(self):
        if self.inTest:
            return self.test_path
        else:
            return self.data_dir

    def check_required_attributes(self):
        if self.inTest is NotImplemented:
            raise NotImplementedError("Subclass must define self.inTest attribute. \n"
                                      + "This attribute should define the DataProvider root directory for files to parse.")

        if self.file_path is NotImplemented:
            raise NotImplementedError("Subclass must define self.file_path attribute. \n"
                                      + "This attribute should define the DataProvider directory for files to parse.")

        if self.file_parser is NotImplemented:
            raise NotImplementedError("Subclass must define self.file_parser attribute. \n"
                                      + "This attribute should define the DataProvider file parser.")

        if self.df is NotImplemented:
            raise NotImplementedError("Subclass must define self.df attribute. \n"
                                      + "This attribute should define the DataProvider pandas.DataFrame.")

        if self.column_types is NotImplemented:
            raise NotImplementedError("Subclass must define self.column_types attribute. \n"
                                      + "This attribute should define the DataProvider column types for the certificate class.")

        if self.column_constraints is NotImplemented:
            raise NotImplementedError("Subclass must define self.column_constraints attribute. \n"
                                      + "This attribute should define the DataProvider column constraints for the certificate class.")

    def filter_fiscalcodes_dataframe(self, cf_column: Union[int, str], inplace=False) -> Union[None, pd.DataFrame]:
        """
        Metodo che filtra il dataframe
        solo per i codici fiscali estratti da Innovation Intelligence

        Parameters:
        ----------

        cf_column : Union[int, str]
            Colonna in cui applicare il filtro, può essere:
            il numero della colonna da filtrare (`int`)
            il nome della colonna da filtrare (`str`)

        inplace : bool, default False
            Se `True` effettua il filtro senza ritornare il DataFrame

        Return:
        -------
        pandas.DataFrame or None 
        """

        if not self.df is NotImplemented:
            cf_list = self.get_fiscalcode_list_from_Anagrafica()

            if isinstance(cf_column, int):
                cond = self.df.iloc[:, cf_column].isin(cf_list)
            elif isinstance(cf_column, str):
                if cf_column in self.df.columns:
                    cond = self.df.loc[:, cf_column].isin(cf_list)
                else:
                    raise KeyError(
                        "Column {} not in self.df.columns".format(cf_column))
            else:
                raise ValueError(
                    "Invalid value for cf_column: {}".format(cf_column))

            df = self.df.loc[cond].copy()
            if inplace:
                self.df = df
            else:
                return df

    def get_fiscalcode_list_from_Anagrafica(self) -> list:
        """
        Estrae la lista dei codici fiscali del DB di Innovation Intelligence
        e li ritorna sotto forma di lista
        """
        try:
            from idb import Anagrafica
        except Exception:
            raise ImportError("Can't import Anagrafica module")

        return Anagrafica().get_fiscalcode_list()

    def get_column_number(self) -> int:
        """
        Metodo che ritorna il numero delle colonne del Data Provider
        """
        if not self.df is NotImplemented:
            return self.df.shape[1]

    def get_column_names(self) -> list:
        """
        Metodo che ritorna il nome delle colonne del Data Provider
        """
        if not self.df is NotImplemented:
            return self.df.columns.tolist()

    def get_column_types(self) -> list:
        """
        Metodo che ritorna la tipologia delle colonne convertite
        da self.get_casted_dataframe()
        """
        if ((not self.df is NotImplemented) and
                (not self.column_types is NotImplemented)):

            return self.get_casted_dataframe().dtypes.tolist()

    def get_casted_dataframe(self) -> pd.DataFrame:
        """
        Metodo che effettua la conversione del file fonte
        secondo indicazione delle colonne per il Data Provider specifico
        """
        if ((not self.df is NotImplemented) and
                (not self.column_types is NotImplemented)):

            columns_casted_to_concat = defaultdict(pd.DataFrame)

            for num, _ in enumerate(self.df.columns):
                col_type = self.column_types.get(num)

                columns_casted_to_concat[num] = DataProvider \
                    .get_casted_column_for_type(
                        self.df.iloc[:, num],
                        col_type
                )

            return pd.concat(columns_casted_to_concat, axis=1)

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
        elif col_type == "date":
            try:
                df_casted = pd.to_datetime(s).to_frame()
            except:
                df_casted = df
        else:
            df_casted = df

        return df_casted

    def get_columns_max_length(self) -> dict:
        """
        Metodo che ritorna la lunghezza massima nelle colonne di un pd.DataFrame
        """
        if not self.df is NotImplemented:

            column_is_max_length_respected_dict = defaultdict(int)

            for num, _ in enumerate(self.df.columns):
                column_is_max_length_respected_dict[num] = DataProvider \
                    .get_column_max_length_is_respected(
                        self.df.iloc[:, num]
                )

            return column_is_max_length_respected_dict

        return {}

    @staticmethod
    def get_column_max_length_is_respected(s: pd.Series) -> int:
        length = s.map(lambda values: DataProvider.get_trimmed_length(values))
        return length.max(axis=0)

    @staticmethod
    def get_trimmed_length(x) -> int:

        cond = DataProvider.catch_null_length(np.isnan, x) | \
            DataProvider.catch_null_length(pd.isnull, x)

        if cond:
            return 0
        else:
            s = str(x).strip()

        return len(s)

    @staticmethod
    def catch_null_length(func, x) -> bool:
        try:
            cond = func(x)
        except TypeError:
            cond = False
        return cond

    def get_column_nullables(self) -> dict:
        """
        Metodo che ritorna True se presenti dei valori mancanti
        False altrimenti 
        """
        def get_column_nullable(s: pd.Series) -> bool:
            return s.isna().any()

        if not self.df is NotImplemented:
            column_is_nullable = defaultdict(bool)

            for num, _ in enumerate(self.df.columns):
                column_is_nullable[num] = get_column_nullable(
                    self.df.iloc[:, num])

            return column_is_nullable
        
        return {}

    def get_column_constraints_is_respected(self) -> pd.Series:
        """
        Metodo che ritorna i duplicati (se presenti) nelle colonne indicate
        dal dizionario in self.column_constraints
        """
        if ((not self.df is NotImplemented) and
                (not self.column_constraints is NotImplemented)):

            columns = [
                col for i, col in enumerate(self.get_column_names())
                if self.column_constraints[i]]

            return self.df.duplicated(subset=columns)  # .sum()  # .shape[0]

        else:
            return pd.Series([])
