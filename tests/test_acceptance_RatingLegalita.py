from certificates import CertificazioniRatingLegalita

import unittest
import numpy as np

class Test_CertificazioniRatingLegalita(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cert = CertificazioniRatingLegalita()
    
    def test_check_file_extension(self):
        self.assertEqual("xlsx", self.cert.check_file_extension())

    def test_check_column_number(self):
        self.assertEqual(8, self.cert.check_column_number())

    def test_check_column_types(self):
        column_types = [
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('<M8[ns]'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('<M8[ns]')
        ]
        self.assertEqual(column_types, self.cert.check_column_types())

    def test_check_column_length(self):
        column_max_length = {
            0: 20,
            1: 11,
            2: None,
            3: None,
            4: None,
            5: 50,
            6: 50,
            7: None
        }
        cert_check_length = self.cert.check_column_length()

        for i, col in enumerate(self.cert.dp.df.columns):
            if column_max_length[i]:
                # Per le colonne con una lunghezza controllata
                with self.subTest(col = col):
                    self.assertGreaterEqual(
                        column_max_length[i], cert_check_length[i])

        self.assertDictEqual

    def test_check_column_nullables(self):
        column_nullables = {
            0: True,
            1: True,
            2: True,
            3: True,
            4: True,
            5: True,
            6: True,
            7: True
        }
        cert_check_nullables = self.cert.check_column_nullables()
        for num, col in enumerate(self.cert.dp.df.columns):
            is_nullable = column_nullables.get(num)
            # Per le colonne False (not nullable) controllo sia False
            with self.subTest(col = col):
                if not is_nullable:
                    self.assertFalse(cert_check_nullables[num])
                else:
                    self.assertTrue(True)
    
    @unittest.skip
    def test_check_column_constrains(self):
        self.assertEqual(0, self.cert.check_column_constraints())