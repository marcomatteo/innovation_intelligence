from tests import TestDataProviderBaseClass
from data_provider import AtecoInfocamere
from file_parser import ParserXls

import unittest
import pandas as pd
import numpy as np

class Test_AtecoInfocamere(TestDataProviderBaseClass):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.dp = AtecoInfocamere(inTest=True)
        cls.file_path = r"data/data_tests/Infocamere/"
        cls.file_parser = ParserXls
        cls.first_row = [
            "00002070324",
            "TS",
            65026,
            0,
            "I",
            "52.29.1",
            "Spedizionieri e agenzie di operazioni doganali"
        ]
        cls.columns = [
            "c fiscale",
            "pv",
            "rea",
            "loc",
            "imp att",
            "ateco 2007",
            "descrizione ateco 2007"
        ]
        cls.column_types = {
            0: "object",        
            1: "object",
            2: "object",
            3: "int",
            4: "object",
            5: "object",
            6: "object",
        }