from data_provider import DataProvider

import unittest
import pandas as pd
import numpy as np
import datetime

class Test_DataProvider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data = {
            'col1': ['    min    ', 'asdasdasd0',
                    '          ciao', 'ciao          '],
            'col2': ['UD', '   O', 'P   ', '   TS    '],
            'col3': [0, 1, 1, 1],
            'col4': ([np.nan] * 3) + [0.24],
            'col5': pd.date_range(start=datetime.datetime.today(), periods=4)
        }
        df = pd.DataFrame(data)

        col_types = {
            0: 'object',
            1: 'object',
            2: 'int',
            3: 'float',
            4: 'date'
        }

        col_constraints = {
            0: False,
            1: False,
            2: True,
            3: False,
            4: False
        }

        cls.dp = DataProvider(df, col_types, col_constraints)

    def test_get_column_number(self):
        self.assertEqual(5, self.dp.get_column_number())

    def test_get_column_number_wrong_number(self):
        self.assertNotEqual(10, self.dp.get_column_number())
        
    def test_get_column_names(self):
        column_names = ['col1','col2','col3','col4','col5']
        self.assertEqual(column_names,
                            self.dp.get_column_names())

    def test_get_column_types(self):
        column_types = [
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('int64'),
            np.dtype('float64'),
            np.dtype('<M8[ns]')
        ]
        self.assertEqual(column_types,
                            self.dp.get_column_types())

    def test_column_constraints_is_respected(self):
        self.assertEqual(2, self.dp.get_column_constraints_is_respected())

    def test_get_column_nullables(self):
        column_nullables = {
            0: False,
            1: False,
            2: False,
            3: True,
            4: False
        }
        self.assertEqual(column_nullables,
                            self.dp.get_column_nullables())

    def test_get_column_max_length(self):
        column_max_length = {
            0: 10,
            1: 2,
            2: 1,
            3: 4,
            4: 26
        }
        self.assertEqual(column_max_length,
                                self.dp.get_columns_max_length())

    def test_get_casted_dataframe(self):
        date_column = pd.date_range(start=datetime.datetime.today(), periods=4)
        
        # Creo dataframe di test, uguale al self.dp.df solo con stringhe 
        data = {
            'col1': ['    min    ', 'asdasdasd0',
                    '          ciao', 'ciao          '],
            'col2': ['UD', '   O', 'P   ', '   TS    '],
            'col3': ['0', '1', '1', '1'],
            'col4': ([np.nan] * 3) + ['0.24'],
            'col5': date_column.strftime("%Y-%m-%d") # Cast date to string
        }
        df = pd.DataFrame(data)

        # Creo DataProvider di test con il dataframe solo di stringhe
        test_dp = DataProvider(df, 
                    self.dp.column_types, self.dp.column_constraints)
                    
        # Effettuo il casting
        casted_df = test_dp.get_casted_dataframe()

        self.assertEqual(casted_df.dtypes.tolist(),
                            self.dp.df.dtypes.tolist())

        