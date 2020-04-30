import pandas as pd
import numpy as np

from idb import DatabaseConnector

class Certificazioni(DatabaseConnector):

    def __init__(self, inTest = True):
        super().__init__(inTest=inTest)
        pass

    def get_data_certificazioni(self) -> pd.DataFrame:
        return self.open_table('DATA_Certificazione')

    def get_tipo_certificazioni(self) -> pd.DataFrame:
        return self.open_table('SVC_Certificazione')

    def get_certificazioni(self) -> pd.DataFrame:
        """
        Open and return Accredia data from the DB

        Returns:
            pd.DataFrame -- as Accredia data provider
        """
        data_df = self.get_data_certificazioni()
        tipo_df = self.get_tipo_certificazioni()

        column_to_cast_dict = {'RF_Certificazione':'float64'}
        
        result = data_df \
            .astype(column_to_cast_dict) \
            .merge(
                    tipo_df, 
                    how = 'left', 
                    left_on = 'RF_Certificazione', 
                    right_on = 'ID_Certificazione'
                )
        
        columns_to_drop = ['ID_DataCertificazione'
                        , 'RF_Importazione'
                        , 'ID_Certificazione'
                        , 'RF_Certificazione'
                        , 'DataInsert'
                        , 'RF_TipoCertificazione']

        return result.drop(columns=columns_to_drop)