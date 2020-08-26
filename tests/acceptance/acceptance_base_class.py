from typing import Dict
import unittest
import logging
from acceptance_builder import AcceptanceBuilder

logger = logging.getLogger(__name__)

class TestAcceptanceBaseClass(unittest.TestCase):

    log_new_line = "-".join(["-"]*10)

    cert = NotImplemented   # type: AcceptanceBuilder

    def log_debug_data(self, data: Dict[str, str]):
        data_to_log_str = self.cert.get_log_list_from_dict(data)
        logger.debug("Check {}".format(data_to_log_str))
    
    def log_exeption_data(self, data: Dict[str, str]):
        data_to_log_str = self.cert.get_log_list_from_dict(data)
        logger.exception("Check {}".format(data_to_log_str))

    def test_check_file_extension(self):

        if (not self.cert is NotImplemented):
            logger.debug("Test file type")

            expected_file_extension = self.cert.dp_file_extension
            cert_file_extension = self.cert.check_file_extension()
            logger.debug("Check {{'file_extension': {}}}".format(cert_file_extension))

            try:
                self.assertEqual(cert_file_extension, expected_file_extension)
            except Exception as e:
                exception = "Wrong file extension: {}".format(
                    cert_file_extension)
                logger.exception(exception)
                raise e
            
            logger.debug("Test OK\n")

    def test_check_column_number(self):

        if (not self.cert is NotImplemented):
            logger.debug("Test column number")

            expected_column_number = self.cert.column_number
            cert_column_number = self.cert.check_column_number()
            logger.debug("Check {{'column_number': {}}}".format(cert_column_number))

            try:
                self.assertEqual(cert_column_number, expected_column_number)
            except Exception as e:
                exception = "Wrong column number: {}".format(
                    cert_column_number)
                logger.exception(exception)
                raise e
            
            logger.debug("Test OK\n")

    def test_check_column_types(self):

        if (not self.cert is NotImplemented):
            logger.debug("Test column types")

            expected_column_types = [col.tipologia for col in self.cert.columns]
            cert_column_types = self.cert.check_column_types()

            data_to_log_dict = {col.nome: str(col.tipologia) for col in self.cert.columns}
            self.log_debug_data(data_to_log_dict)

            try:
                self.assertEqual(cert_column_types, expected_column_types)
            except Exception as e:
                # exception = "Wrong column types:\n{}" \
                #     .format(",\n".join(cert_column_types_to_log))
                logger.exception(e)
                raise e
            
            logger.debug("Test OK\n")

    def test_check_column_length(self):

        if (not self.cert is NotImplemented):
            logger.debug("Test columns max length")

            # expected_column_max_length = self.cert.column_max_length
            expected_column_max_length = [col.lunghezza for col in self.cert.columns]
            cert_check_length = self.cert.check_column_length()

            data_to_log_dict = {col.nome: str(col.lunghezza) for col in self.cert.columns}
            self.log_debug_data(data_to_log_dict)

            # cert_check_lenght_to_log = self.cert.get_log_list_from_list(
            #     cert_check_length)
            # logger.debug("Certificate column lengths:\n{}"
            #              .format(",\n".join(cert_check_lenght_to_log)))

            invalid_column_list = []
            invalid_column_dict = {}
            for i, col in enumerate(self.cert.dp.df.columns):

                if expected_column_max_length[i]:

                    with self.subTest(col=col):
                        try:
                            self.assertLessEqual(
                                cert_check_length[i],
                                expected_column_max_length[i]
                            )
                        except Exception as e:
                            invalid_column_list.append(col)
                            invalid_column_dict[col] = cert_check_length[i]
                            # exception = "Wrong length for {} column." \
                            #     .format(col) + \
                            #     "Expected {} " \
                            #     .format(expected_column_max_length[i])
                            logger.exception(e)
                            raise e
                        
                        logger.debug("Subtest OK")

            try:
                # self.assertEqual(len(invalid_column_list), 0)
                self.assertEqual(len(invalid_column_dict), 0)
            except Exception as e:
                # logger.exception("Found wrong column lengths for {} columns"
                #                  .format(", ".join(invalid_column_list)))
                self.log_exeption_data(invalid_column_dict)
                raise e
            
            logger.debug("Test OK\n")

    def test_check_column_nullables(self):

        if (not self.cert is NotImplemented):
            logger.debug("Test columns nullable condition")

            # expected_column_nullables = self.cert.column_nullables
            expected_column_nullables = [col.nullable for col in self.cert.columns]
            cert_check_nullables = self.cert.check_column_nullables()

            # cert_check_nullables_to_log = self.cert \
            #     .get_log_list_from_list(cert_check_nullables)
            # logger.debug("Certificate column nullables:\n{}"
            #              .format(",\n".join(cert_check_nullables_to_log)))
            data_to_log_dict = {col.nome: str(col.nullable) for col in self.cert.columns}
            self.log_debug_data(data_to_log_dict)

            # invalid_column_list = []
            invalid_column_dict = {}
            for num, col in enumerate(self.cert.dp.df.columns):

                is_nullable = expected_column_nullables[num]
                # Per le colonne False (not nullable) controllo sia False
                if not is_nullable:

                    with self.subTest(col=col):
                        try:
                            self.assertFalse(cert_check_nullables[num])
                        except Exception as e:
                            # invalid_column_list.append(col)
                            invalid_column_dict[col] = cert_check_nullables[num]
                            # exception = "Wrong setup for {} column." \
                            #     .format(col) + \
                            #     "Expected nullable False not True "
                            logger.exception(e)
                            raise e
                        
                        logger.debug("Subtest OK")

            try:
                # self.assertEqual(len(invalid_column_list), 0)
                self.assertEqual(len(invalid_column_dict), 0)
            except Exception as e:
                # logger.exception("Found wrong column nullables for {} columns"
                #                  .format(", ".join(invalid_column_list)))
                self.log_exeption_data(invalid_column_dict)
                raise e
            
            logger.debug("Test OK\n")

    def test_check_column_constraints(self):

        if not self.cert is NotImplemented:
            logger.debug("Test column constraints")
            duplicates = self.cert.get_duplicates()
            
            try:
                self.assertEqual(duplicates.sum(), 0)
            except Exception as e:
                condition = duplicates == True
                logger.error("\n\n{}\n".format(
                    self.cert.dp.df.loc[condition, [col.nome for col in self.cert.columns if col.pk]].to_json()))
                raise e
            
            logger.debug("Test OK\n")
