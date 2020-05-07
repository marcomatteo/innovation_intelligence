from certificates import Certificazioni
from data_provider import Modefinance

import numpy as np

class CertificazioniModefinance(Certificazioni):
    
    def __init__(self):
        self.dp = Modefinance()
        self.dp_file_extension = "csv"
        self.column_number = 4
        self.column_types = [
            np.dtype('O'),
            np.dtype('int64'),
            np.dtype('<M8[ns]'),
            np.dtype('O')
        ]
        self.column_max_length = {
            0: 19,
            1: 6,
            2: 20,
            3: 10,
        }
        self.column_nullables = {
            0: False,
            1: True,
            2: True,
            3: True,
            4: True
        }