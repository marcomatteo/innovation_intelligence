from tests import TestAcceptanceBaseClass
from utilities import create_logger
from acceptance_builder import BilanciBuilder

import logging
from datetime import datetime

# LOG_FILE = datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
# logging.basicConfig(
#     level = logging.DEBUG,
#     format = "%(asctime)s %(levelname)-5s %(name)-8s (%(funcName)s) %(message)s",
#     datefmt = "%d-%m-%Y %H:%M:%S",
#     filename = r"logs/acceptance_tests/BilanciInfocamere/" + LOG_FILE,
#     filemode = "w"
# )

class Test_BilanciInfocamereAcceptance(TestAcceptanceBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.logger = create_logger("BilanciInfocamere")
        # cls.logger = logging.getLogger(__name__)
        cls.cert = BilanciBuilder()
        super().setUpClass()

if __name__ == "__main__":
    from unittest import main
    main(verbosity=2)