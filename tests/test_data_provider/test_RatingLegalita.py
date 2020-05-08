from tests import TestDataProviderBaseClass
from data_provider import RatingLegalita
from file_parser import ParserXls

import unittest
import pandas as pd
from datetime import datetime

class Test_RatingLegalita(TestDataProviderBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.dp = RatingLegalita(inTest=True)
        cls.columns = [
            "Procedimento",
            "Codice fiscale",
            "Sede Legale",
            "Società",
            "Data Decisione",
            "Esito",
            "Rating",
            "Scadenza  Revoca Annullamento Sospensione"
        ]
        cls.first_row = [
            "RT1",
            "00776670895",
            "Priolo Gargallo (SR)",
            "ELEA S.R.L.",
            pd.Timestamp('2019-07-17 00:00:00'),    # "7/17/2019", 
            "Rating Rinnovato",
            "**",
            datetime(2021, 7, 17, 0, 0)   # "7/17/2021"
        ]
        cls.file_path = r"data/data_tests/RatingLegalita/"
        cls.column_types = {
            0: 'object',
            1: 'object',
            2: 'object',
            3: 'object',
            4: 'date',
            5: 'object',
            6: 'object',
            7: 'date'
        }
        cls.file_parser = ParserXls
    

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