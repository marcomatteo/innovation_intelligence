from acceptance_builder import AcceptanceBuilder
from data_provider import Accredia

import numpy as np

class AccrediaBuilder(AcceptanceBuilder):

    def __init__(self):
        self.dp = Accredia()
        self.dp.filter_fiscalcodes_dataframe(inplace=True)

        #TODO: Load database connection
        self.dp_file_extension = "csv"
        self.column_number = 5

        self.column_types = [
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('int64'),
            np.dtype('O')
        ]

        self.column_max_length = {
            0: 19,
            1: 6,
            2: 50,
            3: None,
            4: 2
        }

        self.column_nullables = {
            0: False,
            1: True,
            2: True,
            3: True,
            4: True
        }
        # Potrebbe essere una soluzione alternativa ai tre dizionari
        # self.columns = [AcceptanceBuilder.Columns('fiscalcode', np.dtype('O'), 19, False, True)]