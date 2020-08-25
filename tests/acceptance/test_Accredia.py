from tests.acceptance import TestAcceptanceBaseClass
from acceptance_builder import AccrediaBuilder

import numpy as np
import logging
from datetime import datetime 

LOG_FILE = datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
logging.basicConfig(
    level = logging.DEBUG, # Only debug levels or higher
    format = "%(asctime)s %(levelname)-5s %(name)-8s (%(funcName)s) %(message)s",
    datefmt = "%d-%m-%Y %H:%M:%S",
    filename = r"logs/acceptance_tests/Accredia/" + LOG_FILE,
    filemode = "w"
)

class Test_AccrediaAcceptance(TestAcceptanceBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(__name__)
        cls.cert = AccrediaBuilder()

if __name__ == '__main__':
    from unittest import main
    main(verbosity=2)