from tests import TestDataProviderBaseClass
from file_parser import ParserCsv
from data_provider import Accredia

import unittest
import pandas as pd
import numpy as np

class Test_Accredia(TestDataProviderBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.dp = Accredia()
    
    def test_matching_columns_names(self):
        self.columns = [
            "fiscalcode",
            "annomese",
            "regulation",
            "id_istat_province",
            "istat_province_prcode"
        ]
        super().test_matching_columns_names()

    def test_first_row_matching(self):
        self.first_row = [
            "08587760961",
            "201910",
            "UNI CEI EN ISO/IEC 27001:2017",
            "53",
            "PI"
        ]
        super().test_first_row_matching()

    def test_class_inheritance_from_data_provider(self):
        super().test_class_inheritance_from_data_provider()

    def test_attributes_isinstance_df(self):
        super().test_attributes_isinstance_df()

    def test_attributes_isinstance_file_parser(self):
        self.file_parser = ParserCsv
        super().test_attributes_isinstance_file_parser()
        
    def test_attributes_file_path(self):
        self.file_path = r"data/Accredia/"
        super().test_attributes_file_path()

    def test_attributes_file_parser_separator(self):
        self.file_parser_separator = "|"
        super().test_attributes_file_parser_separator()

    def test_attributes_column_types(self):
        self.column_types = {
            0: 'object',
            1: 'object',
            2: 'object',
            3: 'int',
            4: 'object'
        }
        super().test_attributes_column_types()

    def test_attributes_column_constraints(self):
        self.column_constraints = {
            0: True,
            1: False,
            2: True,
            3: False,
            4: True
        }
        super().test_attributes_column_constraints()
