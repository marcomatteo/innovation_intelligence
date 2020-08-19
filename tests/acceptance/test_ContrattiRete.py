from tests import TestAcceptanceBaseClass
from certificates import CertificazioniContrattiRete

import unittest
import numpy as np
import logging
from datetime import datetime

LOG_FILE = datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
logging.basicConfig(
    level=logging.DEBUG,  # Only debug levels or higher
    format="%(asctime)s %(levelname)-5s %(name)-8s (%(funcName)s) \n%(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    filename=r"logs/txt/" + __name__ + r"/" + LOG_FILE,
    filemode="w"
)


class Test_CertificazioniContrattiRete(TestAcceptanceBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(__name__)
        cls.cert = CertificazioniContrattiRete()
