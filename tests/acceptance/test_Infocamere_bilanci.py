from tests import TestAcceptanceBaseClass
from acceptance_builder import BilanciBuilder

import unittest
import numpy as np
import logging
from datetime import datetime

LOG_FILE = datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s %(levelname)-5s %(name)-8s (%(funcName)s) %(message)s",
    datefmt = "%d-%m-%Y %H:%M:%S",
    filename = r"logs/acceptance_tests/BilanciInfocamere/" + LOG_FILE,
    filemode = "w"
)

class Test_InfocamereBilanciAcceptance(TestAcceptanceBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.logger = logging.getLogger(__name__)
        cls.cert = BilanciBuilder()