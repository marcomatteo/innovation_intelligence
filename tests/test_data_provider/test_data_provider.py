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

    def test_get_trimmed_length_int(self):
        self.assertEqual(self.dp.get_trimmed_length(234), 3,
                                "Integer 234 must have length 3!")
    
    def test_get_trimmed_length_float(self):
        self.assertEqual(self.dp.get_trimmed_length(234.02), 6,
                                "Float 234.02 must have length 6!")
    
    def test_get_trimmed_length_string_with_left_and_right_spaces(self):
        self.assertEqual(self.dp.get_trimmed_length(" Ciao ciao "), 9,
                                "String 'Ciao ciao ' must have length 9!")
    
    def test_get_trimmed_length_string_with_left_spaces(self):
        self.assertEqual(self.dp.get_trimmed_length(" Ciao ciao"), 9,
                                "String 'Ciao ciao ' must have length 9!")
    
    def test_get_trimmed_length_string_with_right_spaces(self):
        self.assertEqual(self.dp.get_trimmed_length("Ciao ciao "), 9,
                                "String 'Ciao ciao ' must have length 9!")
    
    def test_get_trimmed_length_nan(self):
        self.assertFalse(self.dp.get_trimmed_length(np.nan), 
                                "Nan Length must be 0!")
    
    def test_get_trimmed_length_NaT(self):
        self.assertFalse(self.dp.get_trimmed_length(pd.NaT), 
                                "NaT Length must be 0!")

    def test_catch_null_length_isnan(self):
        self.assertTrue(self.dp.catch_null_length(np.isnan, np.nan))

    def test_catch_null_length_isnat_pd_NaT(self):
        self.assertTrue(self.dp.catch_null_length(pd.isnull, pd.NaT))
    
    def test_catch_null_length_isnat_np_datetime(self):
        self.assertTrue(self.dp.catch_null_length(np.isnat, 
                                                np.datetime64("NaT")))
    
    def test_get_column_max_length_is_respected_int_positives(self):
        # Integer values between [0, 200)
        series_obj = pd.Series(
            data = np.random.randint(0, 200, size=(100,)),
            index = range(0,100)
        )
        self.assertEqual(
            DataProvider.get_column_max_length_is_respected(series_obj), 3,
            "Positive integer Series from 0 to 200 must have max length 3!"
        )
    
    def test_get_column_max_length_is_respected_int_negatives(self):
        # Integer values between [-200, 0)
        series_obj = pd.Series(
            data = np.random.randint(-200, 0, size=(100,)),
            index = range(0,100)
        )
        self.assertEqual(
            DataProvider.get_column_max_length_is_respected(series_obj), 4,
            "Negative integer Series from -200 to 0 must have max length 4!"
        )
    
    def test_get_column_max_length_is_respected_float_positives(self):
        # Float values between [0, 200)
        series_obj = pd.Series(
            data = np.around((np.random.random_sample((100,)) * 200)), 
            index = range(0,100)
        )
        self.assertEqual(
            DataProvider.get_column_max_length_is_respected(series_obj), 5,
            "Positive float Series from 0 to 200 (123.45) must have max length 5!"
        )
   
    def test_get_column_max_length_is_respected_float_negatives(self):
        # Float values between [0, 200)
        series_obj = pd.Series(
            data = np.around((np.random.random_sample((100,)) * (- 200))), 
            index = range(0,100)
        )
        self.assertEqual(
            DataProvider.get_column_max_length_is_respected(series_obj), 6,
            "Positive float Series from 0 to 200 (123.45) must have max length 5!"
        )
    
    def test_get_column_max_length_is_respected_str(self):
        # Values between [1, 6)
        rand_int_array = np.random.randint(1,6,size=(100,))
        sample_string = "a"
        # Values from 'a' to 'aaaaa'
        composed_string_list = [
            sample_string * val
            for val in rand_int_array
        ]
        series_obj = pd.Series(
            data = composed_string_list, 
            index = range(0,100)
        )
        self.assertEqual(
            DataProvider.get_column_max_length_is_respected(series_obj), 5,
            "String Series from 'a' to 'aaaaa' must have max length 5!"
        )
    


        