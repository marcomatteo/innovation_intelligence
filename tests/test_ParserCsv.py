import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)

import unittest as test
import pandas as pd
from datetime import datetime

from file_parser import ParserCsv
from logger import TestLogger

class Test_ParserCsv(test.TestCase):
    root_dir = ROOT + r"data/data_tests/IParsers/"

    @classmethod
    def setUpClass(cls):
        file_path = cls.root_dir + "test_file.csv"
        cls.parser = ParserCsv(file_name = file_path, sep="|")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_open_file_columns(self):
        df = self.parser.open_file()
        columns = [
            "fiscalcode", "annomese", "regulation", 
            "id_istat_province", "istat_province_prcode"]

        self.assertEqual(
            df.columns.tolist(),
            columns
        )

