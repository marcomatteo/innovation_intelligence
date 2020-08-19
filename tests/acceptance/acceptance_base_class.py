import unittest
import logging
from certificates import Certificazioni

logger = logging.getLogger(__name__)


class TestAcceptanceBaseClass(unittest.TestCase):

    log_new_line = "-".join(["-"]*10)

    cert = NotImplemented

    def test_check_file_extension(self):

        if (not self.cert is NotImplemented):

            expected_file_extension = self.cert.dp_file_extension
            cert_file_extension = self.cert.check_file_extension()
            logger.debug("Certificate {} file extension"
                         .format(cert_file_extension))

            try:
                self.assertEqual(expected_file_extension, cert_file_extension)
            except Exception as e:
                exception = "Wrong file extension: {}".format(
                    cert_file_extension)
                logger.exception(exception)
                raise e
            else:
                logger.debug("Test OK\n")

    def test_check_column_number(self):

        if (not self.cert is NotImplemented):

            expected_column_number = self.cert.column_number
            cert_column_number = self.cert.check_column_number()
            logger.debug("Certificate {} column number"
                         .format(cert_column_number))

            try:
                self.assertEqual(expected_column_number, cert_column_number)
            except Exception as e:
                exception = "Wrong column number: {}".format(
                    cert_column_number)
                logger.exception(exception)
                raise e
            else:
                logger.debug("Test OK\n")

    def test_check_column_types(self):

        if (not self.cert is NotImplemented):

            expected_column_types = self.cert.column_types
            cert_column_types = self.cert.check_column_types()

            cert_column_types_to_log = self.cert \
                .get_log_list_from_list(cert_column_types)

            logger.debug("Certificate column types: \n{}"
                         .format(",\n".join(cert_column_types_to_log)))

            try:
                self.assertEqual(expected_column_types, cert_column_types)
            except Exception as e:
                exception = "Wrong column types:\n{}" \
                    .format(",\n".join(cert_column_types_to_log))
                logger.exception(exception)
                raise e
            else:
                logger.debug("Test OK\n")

    def test_check_column_length(self):

        if (not self.cert is NotImplemented):

            expected_column_max_length = self.cert.column_max_length
            cert_check_length = self.cert.check_column_length()

            cert_check_lenght_to_log = self.cert.get_log_list_from_dict(
                cert_check_length)
            logger.debug("Certificate column lengths:\n{}"
                         .format(",\n".join(cert_check_lenght_to_log)))

            invalid_column_list = []
            for i, col in enumerate(self.cert.dp.df.columns):

                if expected_column_max_length[i]:

                    with self.subTest(col=col):
                        try:
                            self.assertGreaterEqual(
                                expected_column_max_length[i],
                                cert_check_length[i]
                            )
                        except Exception as e:
                            invalid_column_list.append(col)
                            exception = "Wrong length for {} column." \
                                .format(col) + \
                                "Expected {} " \
                                .format(expected_column_max_length[i])
                            logger.exception(exception)
                            raise e
                        else:
                            logger.debug("Subtest OK")

            try:
                self.assertTrue(len(invalid_column_list) == 0)
            except Exception as e:
                logger.exception("Found wrong column lengths for {} columns"
                                 .format(", ".join(invalid_column_list)))
                raise e
            else:
                logger.debug("Test OK\n")

    def test_check_column_nullables(self):

        if (not self.cert is NotImplemented):

            expected_column_nullables = self.cert.column_nullables
            cert_check_nullables = self.cert.check_column_nullables()

            cert_check_nullables_to_log = self.cert \
                .get_log_list_from_dict(cert_check_nullables)
            logger.debug("Certificate column nullables:\n{}"
                         .format(",\n".join(cert_check_nullables_to_log)))

            invalid_column_list = []
            for num, col in enumerate(self.cert.dp.df.columns):

                is_nullable = expected_column_nullables.get(num)
                # Per le colonne False (not nullable) controllo sia False
                if not is_nullable:

                    with self.subTest(col=col):
                        try:
                            self.assertFalse(cert_check_nullables[num])
                        except Exception as e:
                            invalid_column_list.append(col)
                            exception = "Wrong setup for {} column." \
                                .format(col) + \
                                "Expected nullable False not True "
                            logger.exception(exception)
                            raise e
                        else:
                            logger.debug("Subtest OK")

            try:
                self.assertTrue(len(invalid_column_list) == 0)
            except Exception as e:
                logger.exception("Found wrong column nullables for {} columns"
                                 .format(", ".join(invalid_column_list)))
                raise e
            else:
                logger.debug("Test OK\n")

    def test_check_column_constraints(self):

        if not self.cert is NotImplemented:
            logger.debug("Certificate column constraints... ")
            constraints = self.cert.check_column_constraints()
            try:
                self.assertEqual(0, constraints)
            except Exception as e:
                logger.debug("Found duplicates for column_constraints")
                duplicates = self.cert.dp.get_column_constraints_is_respected()
                condition = duplicates == True
                logger.debug("\n\n{}\n".format(duplicates.loc[condition]))
                raise e
            else:
                logger.debug("Test OK\n")
