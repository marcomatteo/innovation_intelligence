from acceptance_builder import AcceptanceBuilder
from data_provider import AtecoInfocamere

import numpy as np

class AtecoBuilder(AcceptanceBuilder):
    
    def __init__(self):
        self.dp = AtecoInfocamere()
        self.dp_file_extension = "xlsx"
        self.column_number = 7
        self.column_types = [np.dtype('O')] * 3 + \
                            [np.dtype('int64')] + \
                            [np.dtype('O')] * 3

        self.column_max_length = {
            0: 11, 
            1: 6, 
            2: 10, 
            3: None, 
            4: 1, 
            5: 10, 
            6: 200
        }
        self.column_nullables = {i: True for i in range(self.column_number)}
