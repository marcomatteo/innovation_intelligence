from acceptance_builder import AcceptanceBuilder
from data_provider import Accredia

import numpy as np


class AccrediaBuilder(AcceptanceBuilder):

    def __init__(self):
        self.dp = Accredia()
        self.dp.filter_fiscalcodes_dataframe(inplace=True)

        self.dp_file_extension = "csv"
        self.column_number = 5

        # self.column_types = [
        #     np.dtype('O'),
        #     np.dtype('O'),
        #     np.dtype('O'),
        #     np.dtype('int64'),
        #     np.dtype('O')
        # ]

        # self.column_max_length = {
        #     0: 19,
        #     1: 6,
        #     2: 50,
        #     3: None,
        #     4: 2
        # }

        # self.column_nullables = {
        #     0: False,
        #     1: True,
        #     2: True,
        #     3: True,
        #     4: True
        # }

        # Potrebbe essere una soluzione alternativa ai tre dizionari
        self.columns = [
            AcceptanceBuilder.Columns(nome='fiscalcode',
                                      tipologia=np.dtype('O'),
                                      lunghezza=19, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='annomese',
                                      tipologia=np.dtype('O'),
                                      lunghezza=6, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='regulation',
                                      tipologia=np.dtype('O'),
                                      lunghezza=50, nullable=True, pk=True),
            AcceptanceBuilder.Columns(nome='id_istat_province',
                                      tipologia=np.dtype('int64'),
                                      lunghezza=None, nullable=False, pk=False),
            AcceptanceBuilder.Columns(nome='istat_province_prcode',
                                      tipologia=np.dtype('O'),
                                      lunghezza=2, nullable=True, pk=True)
        ]
