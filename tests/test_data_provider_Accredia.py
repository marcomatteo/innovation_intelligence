from data_provider import Accredia, DataProvider
from file_parser import ParserCsv

import unittest
import pandas as pd
import numpy as np

class Test_Accredia(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dp = Accredia()
    # Da cambiare ogni aggiornamento del Data Provider ------------------------
    def test_matching_columns_names(self):
        columns = [
            "fiscalcode",
            "annomese",
            "regulation",
            "id_istat_province",
            "istat_province_prcode"
        ]
        self.assertEqual(columns, self.dp.get_column_names())

    def test_first_row_matching(self):
        data = [
            "08587760961",
            "201910",
            "UNI CEI EN ISO/IEC 27001:2017",
            "53",
            "PI"
        ]
        self.assertEqual(data,
            self.dp.df.iloc[0,:].tolist())
    # -------------------------------------------------------------------------
    def test_class_inheritance_from_data_provider(self):
        self.assertTrue(issubclass(type(self.dp), DataProvider))

    def test_attributes_isinstance_df(self):
        self.assertTrue(isinstance(self.dp.df, pd.DataFrame))

    def test_attributes_isinstance_file_parser(self):
        self.assertTrue(isinstance(self.dp.file_parser, ParserCsv))
    
    def test_attributes_isinstance_file_path(self):
        self.assertTrue(isinstance(self.dp.file_path, str))

    def test_attributes_isinstance_file_parser_sep(self):
        self.assertTrue(isinstance(self.dp.file_parser_sep, str))

    def test_attributes_isinstance_column_types(self):
        self.assertTrue(isinstance(self.dp.column_types, dict))

    def test_attributes_isinstance_column_constraints(self):
        self.assertTrue(isinstance(self.dp.column_constraints, dict))

    def test_attributes_file_path(self):
        file_path = r"data/Accredia/"
        self.assertEqual(file_path, self.dp.file_path)

    def test_attributes_file_parser_separator(self):
        separator = "|"
        self.assertEqual(separator, self.dp.file_parser_sep)

    def test_attributes_column_types(self):
        column_types = {
            0: 'object',
            1: 'object',
            2: 'object',
            3: 'int',
            4: 'object'
        }
        self.assertEqual(column_types, self.dp.column_types)

    def test_attributes_column_constraints(self):
        column_constraints = {
            0: True,
            1: False,
            2: True,
            3: False,
            4: True
        }
        self.assertEqual(column_constraints, self.dp.column_constraints)
