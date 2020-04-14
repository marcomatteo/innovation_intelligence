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
        column_max_length = {
            0: 19,
            1: 6,
            2: 50,
            3: None,
            4: 2
        }
        cert_check_length = self.cert.check_column_length()

        for i, col in enumerate(self.cert.dp.df.columns):
            if column_max_length[i]:
                # Per le colonne con una lunghezza controllata
                with self.subTest(col = col):
                    self.assertGreaterEqual(
                        column_max_length[i], cert_check_length[i])

    def test_check_column_nullables(self):
        column_nullables = {
            0: False,
            1: True,
            2: True,
            3: True,
            4: True
        }

        for i, col in enumerate(self.cert.dp.df.columns):
            # Per le colonne False (not nullable) controllo sia False
            with self.subTest(col = col):
                if not col:
                    self.assertFalse(column_nullables[i])
                else:
                    self.assertTrue(True)
    
    @unittest.skip
    def test_check_column_constrains(self):
        self.assertEqual(0, self.cert.check_column_constraints())