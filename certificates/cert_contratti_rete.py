from data_provider import ContrattiRete
from certificates import Certificazioni

import numpy as np


class CertificazioniContrattiRete(Certificazioni):

    def __init__(self):
        self.dp = ContrattiRete()

        self.dp_file_extension = "xlsx"
        self.column_number = 19
        self.column_types = [
            np.dtype('int64'),
            np.dtype('O'),
            np.dtype('<M8[ns]'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O')
        ]
        self.column_max_length = {
            0: None,
            1: 255,
            2: None,
            3: 50,
            4: 20,
            5: 8000,
            6: 10,
            7: 16,
            8: 8000,
            9: 1,
            10: 50,
            11: 2,
            12: 2,
            13: 2,
            14: 6,
            15: 50,
            16: 8000,
            17: 8000,
            18: 2
        }
        self.column_nullables = {
            i: True for i in range(self.column_number)}
        self.column_nullables[3] = False    # numero repertorio
        self.column_nullables[4] = False    # numero atto
        self.column_nullables[7] = False    # c.f.
