import sys
from utilities import create_logger
from tests import TestAcceptanceBaseClass
from acceptance_builder import ContrattiReteBuilder

class Test_ContrattiReteAcceptance(TestAcceptanceBaseClass):
    LOG_DIR = None

    @classmethod
    def setUpClass(cls):
        cls.logger = create_logger("ContrattiRete", path=cls.LOG_DIR)        
        cls.cert = ContrattiReteBuilder()
        super().setUpClass()

if __name__ == '__main__':
    from unittest import main

    if len(sys.argv) > 1:
        Test_ContrattiReteAcceptance.LOG_DIR = sys.argv.pop()

    main(verbosity=2)