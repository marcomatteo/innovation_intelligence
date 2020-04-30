import unittest
from certificates import Certificazioni

class TestAcceptanceBaseClass(unittest.TestCase):

    cert = NotImplemented
    dp_file_extension = NotImplemented
    column_number = NotImplemented
    column_types = NotImplemented
    column_max_length = NotImplemented
    column_nullables = NotImplemented
    
    def test_check_file_extension(self):
        if ((not self.dp_file_extension is NotImplemented) and
            (not self.cert is NotImplemented)):
            self.assertEqual(self.dp_file_extension, 
                                self.cert.check_file_extension())

    def test_check_column_number(self):
        if ((not self.column_types is NotImplemented) and
            (not self.cert is NotImplemented)):
            self.assertEqual(self.column_number, 
                                self.cert.check_column_number())

    def test_check_column_types(self):
        if ((not self.column_types is NotImplemented) and
            (not self.cert is NotImplemented)):
            self.assertEqual(self.column_types, self.cert.check_column_types())

    def test_check_column_length(self):
        if ((not self.column_max_length is NotImplemented) and
            (not self.cert is NotImplemented)):
            cert_check_length = self.cert.check_column_length()

            for i, col in enumerate(self.cert.dp.df.columns):
                if self.column_max_length[i]:
                    # Per le colonne con una lunghezza controllata
                    with self.subTest(col = col):
                        self.assertGreaterEqual(
                            self.column_max_length[i], cert_check_length[i])

    def test_check_column_nullables(self):
        if ((not self.column_nullables is NotImplemented) and
            (not self.cert is NotImplemented)):
            cert_check_nullables = self.cert.check_column_nullables()
            for num, col in enumerate(self.cert.dp.df.columns):
                is_nullable = self.column_nullables.get(num)
                # Per le colonne False (not nullable) controllo sia False
                with self.subTest(col = col):
                    if not is_nullable:
                        self.assertFalse(cert_check_nullables[num])
                    else:
                        self.assertTrue(True)
    
    @unittest.skip
    def test_check_column_constrains(self):
        if not self.cert is NotImplemented:
            self.assertEqual(0, self.cert.check_column_constraints())