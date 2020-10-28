import sys
from tests import TestAcceptanceBaseClass
from utilities import create_logger
from acceptance_builder import BilanciBuilder

class Test_BilanciInfocamereAcceptance(TestAcceptanceBaseClass):
    LOG_DIR = None

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.logger = create_logger("BilanciInfocamere", cls.LOG_DIR)
        cls.cert = BilanciBuilder()
        super().setUpClass()

if __name__ == "__main__":
    from unittest import main

    if len(sys.argv) > 1:
        Test_BilanciInfocamereAcceptance.LOG_DIR = sys.argv.pop()
    
    main(verbosity=2)