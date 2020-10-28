import sys
from tests import TestAcceptanceBaseClass
from acceptance_builder import AtecoBuilder
from utilities import create_logger

class Test_AtecoInfocamereAcceptance(TestAcceptanceBaseClass):
    LOG_DIR = None

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.logger = create_logger("AtecoInfocamere", cls.LOG_DIR)
        cls.cert = AtecoBuilder()
        super().setUpClass()

if __name__ == "__main__":
    from unittest import main

    if len(sys.argv) > 1:
        Test_AtecoInfocamereAcceptance.LOG_DIR = sys.argv.pop()

    main(verbosity=2)