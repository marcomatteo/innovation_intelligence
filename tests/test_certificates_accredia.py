import unittest
import numpy as np
from certificates import CertificazioniAccredia

class Test_CertificazioniAccredia(unittest.TestCase):

    def setUp(self):
        self.cert = CertificazioniAccredia()

    def tearDown(self):
        del self.cert

    def test_check_file_extension(self):
        self.assertEqual("csv", self.cert.check_file_extension())

    def test_check_column_number(self):
        self.assertEqual(5, self.cert.check_column_number())

    def test_check_column_types(self):
        column_types = [
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('int64'),
            np.dtype('O')
        ]
        self.assertEqual(column_types, self.cert.check_column_types())

    def test_check_column_length(self):
        self.assertEqual(0, self.cert.check_column_length())

    def test_check_column_nullables(self):
        self.assertEqual(0, self.cert.check_column_nullables())
    
    def test_check_column_constrains(self):
        self.assertEqual(0, self.cert.check_column_constrains())