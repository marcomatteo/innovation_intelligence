import sys
from tests import TestAcceptanceBaseClass
from acceptance_builder import AtecoInsielBuilder
from utilities import create_logger

class Test_AtecoInsielAcceptance(TestAcceptanceBaseClass):
    LOG_DIR = None

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.logger = create_logger("AtecoInsiel", cls.LOG_DIR)
        cls.cert = AtecoInsielBuilder()
        super().setUpClass()

if __name__ == "__main__":
    from unittest import main

    if len(sys.argv) > 1:
        AtecoInsielBuilder.LOG_DIR = sys.argv.pop()

    main(verbosity=2)