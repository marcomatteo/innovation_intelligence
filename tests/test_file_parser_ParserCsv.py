from file_parser import ParserCsv
from logger import TestLogger
import unittest as test
import pandas as pd
from datetime import datetime

class Test_ParserCsv(test.TestCase):
    root_dir = r"/mnt/c/Users/buzzulini/Documents/GitHub/I2FVG_scripts/"\
        + r"innovation_intelligence/data/data_tests/IParsers/"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_open_file_semicolon_columns_matching(self):
        file_path = self.root_dir + "test_file2.csv"
        parser = ParserCsv(file_path=file_path)
        df = parser.open_file(sep=";")
        
        self.assertEqual(
            ["fiscal_code", "final_rank", 
            "evaluation_date", "is_consolidated"],
            df.columns.tolist()
        )

    def test_open_file_verticalBar_columns_matching(self):
        file_path = self.root_dir + "test_file.csv"
        parser = ParserCsv(file_path=file_path)
        df = parser.open_file(sep="|")

        self.assertEqual(
            ["fiscalcode", "annomese", "regulation", 
            "id_istat_province", "istat_province_prcode"],
            df.columns.tolist()
        )

if __name__ == '__main__':
    loader = test.TestLoader()
    suite = loader.loadTestsFromTestCase(Test_ParserCsv)
    test.TextTestRunner().run(suite)