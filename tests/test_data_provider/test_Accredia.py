from tests import TestDataProviderBaseClass
from file_parser import ParserCsv
from data_provider import Accredia

import unittest
import pandas as pd
import numpy as np

class Test_Accredia(TestDataProviderBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.dp = Accredia(inTest=True)
        cls.file_parser = ParserCsv
        cls.file_path = r"data/data_tests/Accredia/"
        cls.file_parser_separator = "|"
        
        cls.first_row = [
            "08587760961",
            "201910",
            "UNI CEI EN ISO/IEC 27001:2017",
            "53",
            "PI"
        ]
        
        cls.column_types = {
            0: 'object',
            1: 'object',
            2: 'object',
            3: 'int',
            4: 'object'
        }
        
        cls.columns = [
            "fiscalcode",
            "annomese",
            "regulation",
            "id_istat_province",
            "istat_province_prcode"
        ]
        
        cls.column_constraints = {
            0: True,
            1: False,
            2: True,
            3: False,
            4: True
        }

    