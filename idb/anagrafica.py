import pandas as pd
import numpy as np

from idb import DatabaseConnector
from utilities import trim_columns_spaces

class Anagrafica(DatabaseConnector):

    unique_columns = ['CF', 'Provincia', 'SedeUL']

    def __init__(self, inTest = True):
        super().__init__(inTest=inTest)
        pass

    def get_fiscalcode_list(self) -> list:
        query = "SELECT DISTINCT CF FROM DATA_Impresa"
        cf = self.get_dataframe_from_query(query)
        return cf['CF'].tolist()

    def get_sedi_imprese(self):
        return self.get_dataframe_from_table("DATA_Impresa")

    def get_unique_columns(self) -> pd.DataFrame:
        columns = ", ".join(self.unique_columns)

        query = f"""
            ( SELECT {columns}, Denominazione FROM DATA_Impresa )
            UNION 
            ( SELECT {columns}, Denominazione FROM DATA_UnitaLocale )"""

        result = self.get_dataframe_from_query(query)

        return result.apply(lambda col: trim_columns_spaces(col))