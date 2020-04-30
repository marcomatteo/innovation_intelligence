from __future__ import annotations

import pandas as pd
from idb import Anagrafica, Certificazioni

# from utilities import Singleton

class InnovationIntelligence:
    """
    InnovationIntelligence is the interface to the
    database that stores all the informations about firms.

    It can be use a builder class for a high dimensional
    DataFrame with many configurations as are the informations 
    stored in the Innovation Intelligence DB.    
    
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    @staticmethod
    def connect() -> InnovationIntelligence:
        anag = Anagrafica() 
        df = anag.get_sedi_imprese()
        df.set_index('CF', inplace=True)
        return InnovationIntelligence(df)

    def add_dataframe(self, 
                df: pd.DataFrame, 
                *args, **kwargs
            ) -> pd.DataFrame:

        return df.merge(self.df, *args, **kwargs)

    def add_certificazioni(self) -> InnovationIntelligence:
        certificazioni_df = Certificazioni().get_certificazioni()
        
        try:
            new_df = self.add_dataframe(certificazioni_df)
        except:
            print("Can not merge certificazioni in self.df")
            new_df = self.df

        return InnovationIntelligence(new_df)