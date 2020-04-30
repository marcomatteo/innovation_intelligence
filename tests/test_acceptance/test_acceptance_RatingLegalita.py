from tests import TestAcceptanceBaseClass
from certificates import CertificazioniRatingLegalita

import unittest
import numpy as np

class Test_CertificazioniRatingLegalita(TestAcceptanceBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.cert = CertificazioniRatingLegalita()
    
    def test_check_file_extension(self):
        self.dp_file_extension = "xlsx"
        super().test_check_file_extension()

    def test_check_column_number(self):
        self.column_number = 8
        super().test_check_column_number()

    def test_check_column_types(self):
        self.column_types = [
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('<M8[ns]'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('<M8[ns]')
        ]
        super().test_check_column_types()

    def test_check_column_length(self):
        self.column_max_length = {
            0: 20,
            1: 11,
            2: None,
            3: None,
            4: None,
            5: 50,
            6: 50,
            7: None
        }
        super().test_check_column_length()
        
    def test_check_column_nullables(self):
        self.column_nullables = {
            0: True,
            1: True,
            2: True,
            3: True,
            4: True,
            5: True,
            6: True,
            7: True
        }
        super().test_check_column_nullables()
        
    @unittest.skip
    def test_check_column_constrains(self):
        super().test_check_column_constrains()