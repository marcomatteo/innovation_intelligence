import sys
import logging
import unittest as test
import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO

sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")

from data_providers import Accredia
from db_interface import I2FVG, Certificazione
from log_test import LogCaptureRunner, BaseTestCase

LOG_FILE = "tests/logs/certificazioni/accredia.md"
logging.basicConfig(
    level = logging.DEBUG, # Only debug levels or higher
    format = "%(asctime)s %(levelname)-8s (%(funcName)s) %(message)s",
    datefmt = "%d-%m-%Y %H:%M:%S",
    filename = LOG_FILE,
    filemode = "w"
)

class Test_AnagraficaInfocamere(BaseTestCase):
    # Data Provider file name
    dp_file_name = "20200203_accredia.csv"

    @classmethod
    def setUpClass(cls):
        anno = datetime.now().year()
        # Create logger
        cls.logger = logging.getLogger(__name__)    
        cls.logger.info("\n\n## Test Certificazione Data Provider : Accredia {}\n{}\n".format(
            anno, super().log_new_line
        ))

        cls.data_provider = Accredia(cls.dp_file_name)
        cls.ii = I2FVG(True)
        

