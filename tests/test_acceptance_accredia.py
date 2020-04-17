from tests import TestAcceptanceBaseClass
from certificates import CertificazioniAccredia

import unittest
import numpy as np

class Test_CertificazioniAccredia(TestAcceptanceBaseClass):

    @classmethod
    def setUpClass(self):
        self.cert = CertificazioniAccredia()

    def test_check_file_extension(self):
        self.dp_file_extension = "csv"
        super().test_check_file_extension()

    def test_check_column_number(self):
        self.column_number = 5
        super().test_check_column_number()

    def test_check_column_types(self):
        self.column_types = [
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('int64'),
            np.dtype('O')
        ]
        super().test_check_column_types()

    def test_check_column_length(self):
        self.column_max_length = {
            0: 19,
            1: 6,
            2: 50,
            3: None,
            4: 2
        }
        super().test_check_column_length()

    def test_check_column_nullables(self):
        self.column_nullables = {
            0: False,
            1: True,
            2: True,
            3: True,
            4: True
        }
        super().test_check_column_nullables()
    
    @unittest.skip
    def test_check_column_constrains(self):
        super().test_check_column_constrains()