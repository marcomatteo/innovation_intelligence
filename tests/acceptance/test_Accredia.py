import sys
from tests.acceptance import TestAcceptanceBaseClass
from acceptance_builder import AccrediaBuilder
from utilities import create_logger
import unittest

class Test_AccrediaAcceptance(TestAcceptanceBaseClass):
    LOG_DIR = None

    @classmethod
    def setUpClass(cls):
        cls.logger = create_logger("Accredia", path=cls.LOG_DIR)
        cls.cert = AccrediaBuilder()
        super().setUpClass()

    @unittest.skip
    def test_check_column_constraints(self):
        pass

if __name__ == '__main__':
    from unittest import main

    if len(sys.argv) > 1:
        Test_AccrediaAcceptance.LOG_DIR = sys.argv.pop()

    main(verbosity=2)