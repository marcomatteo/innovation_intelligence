from tests import TestDataProviderBaseClass
from file_parser import ParserCsv
from data_provider import Modefinance

import unittest
import pandas as pd
import numpy as np

class Test_Modefinance(TestDataProviderBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.dp = Modefinance(inTest=True)
        cls.file_parser = ParserCsv
        cls.file_path = r"data/data_tests/Modefinance/"
        cls.file_parser_separator = ";"
        cls.columns = [
            'fiscal_code',
            'final_rank',
            'evaluation_date',
            'is_consolidated'
        ]
        cls.first_row = [
            '00002070324',
            '8',
            '01/07/2018',
            'False'
        ]
        cls.column_types = {
            0: 'object',
            1: 'int',
            2: 'date',
            3: 'object'
        }
        cls.column_constraints = {
            0: True,
            1: False,
            2: True,
            3: False
        }