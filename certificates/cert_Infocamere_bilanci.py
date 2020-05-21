from certificates import Certificazioni
from data_provider import BilanciInfocamere

import numpy as np

class CertificazioneBilanci(Certificazioni):
    
    def __init__(self):
        self.dp = BilanciInfocamere()
        self.dp.df = self.dp.df.iloc[:, :16]
        self.dp_file_extension = "xlsx"
        self.column_number = 16
        self.column_types = [
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('int64')] + [np.dtype('float64')] * 12
            
        self.column_max_length = {i: None for i in range(self.column_number)}
        self.column_max_length[0] = 11
        self.column_max_length[1] = 6
        self.column_max_length[2] = 10

        self.column_nullables = {i: True for i in range(self.column_number)}
        self.column_nullables[0] = False
        self.column_nullables[1] = False
        self.column_nullables[3] = False
