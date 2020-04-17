from tests import TestAcceptanceBaseClass
from certificates import CertificazioniModefinance

import unittest
import numpy as np

class Test_CertificazioniModefinance(TestAcceptanceBaseClass):

    @classmethod
    def setUpClass(self):
        self.cert = CertificazioniModefinance()

    def test_check_file_extension(self):
        self.dp_file_extension = "csv"
        super().test_check_file_extension()

    def test_check_column_number(self):
        self.column_number = 4
        super().test_check_column_number()

    def test_check_column_types(self):
        self.column_types = [
            np.dtype('O'),
            np.dtype('int64'),
            np.dtype('<M8[ns]'),
            np.dtype('O')
        ]
        super().test_check_column_types()

    def test_check_column_length(self):
        self.column_max_length = {
            0: 19,
            1: 6,
            2: 20,
            3: 10,
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