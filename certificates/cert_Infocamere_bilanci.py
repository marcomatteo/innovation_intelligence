from certificates import Certificazioni
from data_provider import BilanciInfocamere

import numpy as np

class CertificazioneBilanci(Certificazioni):
    
    def __init__(self):
        self.dp = BilanciInfocamere()
        self.dp_file_extension = "xlsx"
        self.column_number = 0
        self.column_types = []
        self.column_max_length = {}
        self.column_nullables = {}