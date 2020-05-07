from data_provider import RatingLegalita, DataProvider
from file_parser import ParserXls

import unittest
import pandas as pd
from datetime import datetime

class Test_RatingLegalita(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dp = RatingLegalita()
        
    # Da cambiare ogni aggiornamento del Data Provider ------------------------
    def test_matching_columns_names(self):
        columns = [
            "Procedimento",
            "Codice fiscale",
            "Sede Legale",
            "Società",
            "Data Decisione",
            "Esito",
            "Rating",
            "Scadenza  Revoca Annullamento Sospensione"
        ]
        self.assertEqual(columns, self.dp.get_column_names())

    def test_first_row_matching(self):
        data = [
            "RT1",
            "00776670895",
            "Priolo Gargallo (SR)",
            "ELEA S.R.L.",
            pd.Timestamp('2019-07-17 00:00:00'),    # "7/17/2019", 
            "Rating Rinnovato",
            "**",
            datetime(2021, 7, 17, 0, 0)   # "7/17/2021"
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
        file_path = r"data/RatingLegalita/"
        self.assertEqual(file_path, self.dp.file_path)

    def test_attributes_column_types(self):
        column_types = {
            0: 'object',
            1: 'object',
            2: 'object',
            3: 'object',
            4: 'date',
            5: 'object',
            6: 'object',
            7: 'date'
        }
        self.assertEqual(column_types, self.dp.column_types)

    def test_method_update_rating_column_with_spaces(self):
        column = [
            "** ",
            "* ++",
            "* ++",
            "* ++",
            "** ++"
        ]
        self.dp.update_rating_column_with_spaces()
        self.assertEqual(column, self.dp.df["Rating"].head().tolist())