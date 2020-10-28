from tests import TestAcceptanceBaseClass
from acceptance_builder import RatingLegalitaBuilder
from utilities import create_logger
import sys

class Test_RatingLegalitaAcceptance(TestAcceptanceBaseClass):
    LOG_DIR = None

    @classmethod
    def setUpClass(cls):
        cls.logger = create_logger("RatingLegalita", path=cls.LOG_DIR)
        cls.cert = RatingLegalitaBuilder()
        super().setUpClass()

if __name__ == '__main__':
    from unittest import main

    if len(sys.argv) > 1:
        Test_RatingLegalitaAcceptance.LOG_DIR = sys.argv.pop()

    main(verbosity=2)