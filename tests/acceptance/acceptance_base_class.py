from json import dumps, loads
from typing import Dict
import unittest

from acceptance_builder import AcceptanceBuilder

class TestAcceptanceBaseClass(unittest.TestCase):

    cert = NotImplemented   # type: AcceptanceBuilder

    @classmethod
    def setUpClass(cls) -> None:
        if not cls.cert is NotImplemented:
            columns = [str(col) for col in cls.cert.columns]
            cls.logger.debug("Column constraints:\n\t{}\n".format(",\n\t".join(columns)))
            cls.logger.debug("Column number constraint: {}\n".format(str(cls.cert.column_number)))
            cls.logger.debug("File type extension: {}\n".format(cls.cert.dp_file_extension))
            cls.logger.debug("Data Provider:\n{}\n\n".format(cls.cert.dp))
            cls.logger.debug("Begin Test:\n{}".format(" ".join(["-" for _ in range(30)])))

    def log_debug_data(self, data: Dict[str, str]):
        if not self.cert is NotImplemented:
            data_to_log_str = self.cert.get_log_list_from_dict(data)
            data_to_dump = loads(data_to_log_str)
            data_to_log = dumps(data_to_dump, indent=4)
            self.logger.debug("Values: \n{}\n".format(data_to_log))

    def subtest(self, tocert: list, expected: list, func):
        def config(i):
            exp_value = expected[i]

            if func == self.assertFalse:
                # if nullable is False -> do the subtest
                cond = not exp_value
                params = [tocert[i]]
            else:
                # can be None for testing columns max length
                cond = exp_value
                params = [tocert[i], exp_value]
            
            return cond, params
        
        if not self.cert is NotImplemented:
            failures = {}

            for i, col in enumerate(self.cert.dp.df.columns):
                cond, params = config(i)

                if cond:
                    with self.subTest(col=col):
                        try:
                            func(*params)
                        except Exception as e:
                            failures[col] = tocert[i]
                            
                            exception = 'Subtest col "{}" NOT OK, check value_counts()'.format(col)
                            msg = "Subtest failed, check the column values."
                            
                            self.logger.exception(exception + "\n\n")
                            self.logger.debug(msg + "\n\n")
                            self.fail(msg)

                        self.logger.debug('Subtest col "{}" OK'.format(col))

            return self.endtest(failures)

    def endtest(self, failures: dict) -> None:
        if not self.cert is NotImplemented:
            try:
                self.assertEqual(len(failures), 0)
            except Exception as e:
                self.log_debug_data(failures)
                self.fail("Test failed. Check the file.")

            self.logger.debug("Test OK\n\n")

    def test_check_file_extension(self):

        if (not self.cert is NotImplemented):
            self.logger.debug("Test file type")

            expected_file_extension = self.cert.dp_file_extension
            cert_file_extension = self.cert.check_file_extension()
            self.logger.debug('Check {{"file_extension": "{}"}}'.format(cert_file_extension))

            try:
                self.assertEqual(cert_file_extension, expected_file_extension)
            except Exception as e:
                exception = "Wrong file extension: {}".format(
                    cert_file_extension)
                
                msg = "Wrong file extension. Check the file."
                self.logger.exception("\n" + exception + "\n\n")
                self.logger.debug(msg + "\n\n")
                self.fail(msg)
            
            self.logger.debug("Test OK\n\n")

    def test_check_column_number(self):

        if (not self.cert is NotImplemented):
            self.logger.debug("Test column number")

            expected_column_number = self.cert.column_number
            cert_column_number = self.cert.check_column_number()
            self.logger.debug('Check {{"column_number": {}}}'.format(cert_column_number))

            try:
                self.assertEqual(cert_column_number, expected_column_number)
            except Exception as e:
                exception = "Wrong column number: {}".format(
                    cert_column_number)
                
                msg = "Wrong column number. Check the file."
                self.logger.exception("\n" + exception + "\n\n")
                self.logger.debug(msg + "\n\n")
                self.fail(msg)
            
            self.logger.debug("Test OK\n\n")

    def test_check_column_types(self):

        if (not self.cert is NotImplemented):
            self.logger.debug("Test column types")

            expected_column_types = [col.tipologia for col in self.cert.columns]
            cert_column_types = self.cert.check_column_types()

            self.subtest(
                tocert=cert_column_types, 
                expected=expected_column_types, 
                func=self.assertEqual)

    def test_check_column_length(self):

        if (not self.cert is NotImplemented):
            self.logger.debug("Test columns max length")

            expected_column_max_length = [col.lunghezza for col in self.cert.columns]
            cert_check_length = self.cert.check_column_length()

            self.subtest(
                tocert=cert_check_length, expected=expected_column_max_length, 
                func=self.assertLessEqual)

    def test_check_column_nullables(self):

        if (not self.cert is NotImplemented):
            self.logger.debug("Test columns nullable condition")

            expected_column_nullables = [col.nullable for col in self.cert.columns]
            cert_check_nullables = self.cert.check_column_nullables()
            
            self.subtest(
                tocert=cert_check_nullables, 
                expected=expected_column_nullables,
                func=self.assertFalse)

    def test_check_column_constraints(self):

        if not self.cert is NotImplemented:
            self.logger.debug("Test column constraints")
            duplicates = self.cert.get_duplicates()
            
            try:
                self.assertEqual(duplicates.sum(), 0)
            except Exception as e:
                condition = duplicates == True
                columns = [num for num, col in enumerate(self.cert.columns) if col.pk]
                
                data_to_parse = self.cert.dp.df.loc[condition].iloc[:, columns].to_json(orient="index")
                data_to_dump = loads(data_to_parse)
                data_to_log = dumps(data_to_dump, indent=4)

                msg = "Duplicates founded. Check the file."
                self.logger.exception("\n{}\n\n".format(data_to_log))
                self.logger.debug(msg + "\n\n")
                self.fail(msg)
            
            self.logger.debug("Test OK\n\n")
