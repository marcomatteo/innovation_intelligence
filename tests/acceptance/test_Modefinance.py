import sys
from utilities import create_logger
from tests import TestAcceptanceBaseClass
from acceptance_builder import ModefinanceBuilder

class Test_ModefinanceAcceptance(TestAcceptanceBaseClass):
    LOG_DIR = None

    @classmethod
    def setUpClass(cls):
        cls.logger = create_logger("Modefinance", path=cls.LOG_DIR)
        cls.cert = ModefinanceBuilder()
        super().setUpClass()

if __name__ == '__main__':
    from unittest import main

    if len(sys.argv) > 1:
        Test_ModefinanceAcceptance.LOG_DIR = sys.argv.pop()

    main(verbosity=2)