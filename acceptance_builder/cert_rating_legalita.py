from data_provider.data_provider import DataProvider

import pandas as pd
from data_provider import RatingLegalita
from acceptance_builder import AcceptanceBuilder

import numpy as np


class RatingLegalitaBuilder(AcceptanceBuilder):

    def __init__(self):
        self.dp = RatingLegalita()
        self.dp.filter_fiscalcodes_dataframe(inplace=True)
        self.dp_file_extension = "xlsx"
        self.column_number = 8
        self.columns = [
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype('O'),  lunghezza=20, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype('O'), lunghezza=11, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype('O'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype('O'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype('O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype('O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False)
        ]

    def check_column_types(self) -> list:
        """
        Sovrascrivo il metodo per il Rating di Legalità perché
        l'ultima colonna (Scadenza  Revoca Annullamento Sospensione)
        contiene date e, dove non è specificato, un valore anomalo '(*)'
        che viene già gestito dal DB.

        Returns:
            list: lista di tipologie in formato np.dtypes()
        """
        dp_copy = DataProvider(
            df=self.dp.df.copy(deep=True),
            column_types=self.dp.column_types,
            column_constraints=self.dp.column_constraints)

        column_to_mask_name = self.dp.df.columns.tolist()[-1]

        date_filter = self.dp.df[column_to_mask_name] == '(*)'
        dp_copy.df[column_to_mask_name].mask(date_filter, pd.NaT, inplace=True)

        return dp_copy.get_column_types()
