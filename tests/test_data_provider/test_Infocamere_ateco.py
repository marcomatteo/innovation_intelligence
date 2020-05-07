import unittest
from data_provider import AtecoInfocamere, DataProvider
from file_parser import ParserXls
import pandas as pd
import numpy as np

class Test_AtecoInfocamere(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.dp = AtecoInfocamere()

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    # Da cambiare ogni aggiornamento del Data Provider ------------------------
    def test_matching_columns_names(self):
        columns = [
            "c fiscale",
            "pv",
            "rea",
            "loc",
            "imp att",
            "ateco 2007",
            "descrizione ateco 2007"
        ]
        self.assertEqual(columns, self.dp.get_column_names())

    def test_first_row_matching(self):
        data = [
            "00002070324",
            "TS",
            65026,
            0,
            "I",
            "52.29.1",
            "Spedizionieri e agenzie di operazioni doganali"
        ]
        self.assertEqual(data,
            self.dp.df.iloc[0,:].tolist())
    # -------------------------------------------------------------------------
    def test_class_inheritance_from_data_provider(self):
        self.assertTrue(issubclass(type(self.dp), DataProvider))

    def test_attributes_isinstance_df(self):
        self.assertTrue(isinstance(self.dp.df, pd.DataFrame))

    def test_attributes_isinstance_file_parser(self):
        self.assertTrue(isinstance(self.dp.file_parser, ParserXls))
    
    def test_attributes_isinstance_file_path(self):
        self.assertTrue(isinstance(self.dp.file_path, str))

    def test_attributes_isinstance_column_types(self):
        self.assertTrue(isinstance(self.dp.column_types, dict))

    def test_attributes_file_path(self):
        file_path = r"data/Infocamere/"
        self.assertEqual(file_path, self.dp.file_path)

    def test_attributes_column_types(self):
        column_types = {
            0: "object",        
            1: "object",
            2: "object",
            3: "object",
            4: "object",
            5: "object",
            6: "object",
        }
        self.assertEqual(column_types, self.dp.column_types)