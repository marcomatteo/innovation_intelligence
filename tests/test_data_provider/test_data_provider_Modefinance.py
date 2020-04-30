from tests import TestDataProviderBaseClass
from file_parser import ParserCsv
from data_provider import Modefinance

import unittest
import pandas as pd
import numpy as np

class Test_Modefinance(TestDataProviderBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.dp = Modefinance()
    
    def test_matching_columns_names(self):
        self.columns = [
            'fiscal_code',
            'final_rank',
            'evaluation_date',
            'is_consolidated'
        ]
        super().test_matching_columns_names()

    def test_first_row_matching(self):
        self.first_row = [
            '00002070324',
            '8',
            '01/07/2018',
            'False'
        ]
        super().test_first_row_matching()
        
    def test_attributes_file_path(self):
        self.file_path = r"data/Modefinance/"
        super().test_attributes_file_path()

    def test_attributes_column_types(self):
        self.column_types = {
            0: 'object',
            1: 'int',
            2: 'date',
            3: 'object'
        }
        super().test_attributes_column_types()

    def test_attributes_column_constraints(self):
        self.column_constraints = {
            0: True,
            1: False,
            2: True,
            3: False
        }
        super().test_attributes_column_constraints()
    
    def test_attributes_file_parser_separator(self):
        self.file_parser_separator = ";"
        super().test_attributes_file_parser_separator()

    def test_class_inheritance_from_data_provider(self):
        super().test_class_inheritance_from_data_provider()

    def test_attributes_isinstance_df(self):
        super().test_attributes_isinstance_df()

    def test_attributes_isinstance_file_parser(self):
        self.file_parser = ParserCsv
        super().test_attributes_isinstance_file_parser()