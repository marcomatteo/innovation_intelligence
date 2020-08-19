import unittest
from unittest.mock import Mock, MagicMock, patch

import pandas as pd
from pandas import util
import numpy as np
import datetime

from data_provider import DataProvider


class Test_DataProvider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data = {
            'col1': ['    min    ', 'asdasdasd0', '          ciao', 'ciao          '],
            'col2': ['UD', '   O', 'P   ', '   TS    '],
            'col3': [0, 1, 1, 1],
            'col4': ([np.nan] * 3) + [0.24],
            'col5': pd.date_range(start=datetime.datetime.today(), periods=4)
        }
        df = pd.DataFrame(data)

        col_types = {0: 'object', 1: 'object', 2: 'int', 3: 'float', 4: 'date'}

        col_constraints = {0: False, 1: False, 2: True, 3: False, 4: False}
        cls.dp = DataProvider(df, col_types, col_constraints)

    def test_root_path(self):
        self.dp.inTest = True
        self.assertEqual(self.dp.root_path, r"data/data_tests/")
        self.dp.inTest = False
        self.assertEqual(self.dp.root_path, r"data/")

    def test_get_column_number(self):
        self.assertEqual(self.dp.get_column_number(), 5)
        self.assertNotEqual(self.dp.get_column_number(), 10)

    def test_get_column_names(self):
        self.assertEqual(self.dp.get_column_names(), 
                        ['col1', 'col2', 'col3', 'col4', 'col5'])

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
        from data_provider import DataProvider
        date_column = pd.date_range(start=datetime.datetime.today(), periods=4)

        # Creo dataframe di test, uguale al self.dp.df solo con stringhe
        data = {
            'col1': ['    min    ', 'asdasdasd0',
                     '          ciao', 'ciao          '],
            'col2': ['UD', '   O', 'P   ', '   TS    '],
            'col3': ['0', '1', '1', '1'],
            'col4': ([np.nan] * 3) + ['0.24'],
            'col5': date_column.strftime("%Y-%m-%d")  # Cast date to string
        }
        df = pd.DataFrame(data)

        # Creo DataProvider di test con il dataframe solo di stringhe
        test_dp = DataProvider(df,
                               self.dp.column_types, self.dp.column_constraints)

        # Effettuo il casting
        casted_df = test_dp.get_casted_dataframe()

        self.assertEqual(casted_df.dtypes.tolist(),
                         self.dp.df.dtypes.tolist())

    def test_get_trimmed_length(self):
        self.assertEqual(self.dp.get_trimmed_length(234), 3,
                         "Integer 234 must have length 3!")
        self.assertEqual(self.dp.get_trimmed_length(234.02), 6,
                         "Float 234.02 must have length 6!")
        self.assertEqual(self.dp.get_trimmed_length(" Ciao ciao "), 9,
                         "String 'Ciao ciao ' must have length 9!")
        self.assertEqual(self.dp.get_trimmed_length(" Ciao ciao"), 9,
                         "String 'Ciao ciao ' must have length 9!")
        self.assertEqual(self.dp.get_trimmed_length("Ciao ciao "), 9,
                         "String 'Ciao ciao ' must have length 9!")
        self.assertFalse(self.dp.get_trimmed_length(np.nan),
                         "Nan Length must be 0!")
        self.assertFalse(self.dp.get_trimmed_length(pd.NaT),
                         "NaT Length must be 0!")

    def test_catch_null_length_isnan(self):
        self.assertTrue(self.dp.catch_null_length(np.isnan, np.nan))
        self.assertTrue(self.dp.catch_null_length(pd.isnull, pd.NaT))
        self.assertTrue(self.dp.catch_null_length(np.isnat,
                                                  np.datetime64("NaT")))

    def test_get_column_max_length_is_respected_int_positives(self):
        from data_provider import DataProvider
        # Integer values between [0, 200)
        series_obj = pd.Series(
            data=np.random.randint(0, 200, size=(100,)),
            index=range(0, 100)
        )
        self.assertEqual(
            DataProvider.get_column_max_length_is_respected(series_obj), 3,
            "Positive integer Series from 0 to 200 must have max length 3!"
        )

    def test_get_column_max_length_is_respected_int_negatives(self):
        from data_provider import DataProvider
        # Integer values between [-200, 0)
        series_obj = pd.Series(
            data=np.random.randint(-200, 0, size=(100,)),
            index=range(0, 100)
        )
        self.assertEqual(
            DataProvider.get_column_max_length_is_respected(series_obj), 4,
            "Negative integer Series from -200 to 0 must have max length 4!"
        )

    def test_get_column_max_length_is_respected_float_positives(self):
        from data_provider import DataProvider
        # Float values between [0, 200)
        series_obj = pd.Series(
            data=np.around((np.random.random_sample((100,)) * 200)),
            index=range(0, 100)
        )
        self.assertEqual(
            DataProvider.get_column_max_length_is_respected(series_obj), 5,
            "Positive float Series from 0 to 200 (123.45) must have max length 5!"
        )

    def test_get_column_max_length_is_respected_float_negatives(self):
        from data_provider import DataProvider
        # Float values between [0, 200)
        series_obj = pd.Series(
            data=np.around((np.random.random_sample((100,)) * (- 200))),
            index=range(0, 100)
        )
        self.assertEqual(
            DataProvider.get_column_max_length_is_respected(series_obj), 6,
            "Positive float Series from 0 to 200 (123.45) must have max length 5!"
        )

    def test_get_column_max_length_is_respected_str(self):
        from data_provider import DataProvider
        # Values between [1, 6)
        rand_int_array = np.random.randint(1, 6, size=(100,))
        sample_string = "a"
        # Values from 'a' to 'aaaaa'
        composed_string_list = [
            sample_string * val
            for val in rand_int_array
        ]
        series_obj = pd.Series(
            data=composed_string_list,
            index=range(0, 100)
        )
        self.assertEqual(
            DataProvider.get_column_max_length_is_respected(series_obj), 5,
            "String Series from 'a' to 'aaaaa' must have max length 5!"
        )

    @patch("data_provider.DataProvider.get_fiscalcode_list_from_Anagrafica")
    def test_filter_fiscalcodes_dataframe_int(self, mock_method):
        # Creo lista di codici fiscali fittizzi, solo i primi 2 corrispondono
        mocked_list = ['08587760961', '02538160033', 
                   '10536370017', 'MRCNTN63H03G942C']
        mock_method.return_value = mocked_list

        # Creo DataProvider di Test
        data = {
            'col1': ['08587760961', '02538160033', '05903120631', '02643150168'],
            'col2': ['UD', 'O', 'P', 'TS']
        }
        df = pd.DataFrame(data)
        col_types = {0: 'object', 1: 'object'}
        col_constraints = {0: True, 1: False}
        dp = DataProvider(df, col_types, col_constraints)

        # Richiamo il metodo da testare inplace
        dp.filter_fiscalcodes_dataframe(0, inplace=True)

        # Richiamo il metodo da testare con return value
        new_df = dp.filter_fiscalcodes_dataframe(0, inplace=False)

        mock_method.assert_called()

        # Effettuo il test
        pd.testing.assert_frame_equal(dp.df, pd.DataFrame(
            {'col1': ['08587760961', '02538160033'], 'col2': ['UD', 'O']}))
        pd.testing.assert_frame_equal(new_df, pd.DataFrame(
            {'col1': ['08587760961', '02538160033'], 'col2': ['UD', 'O']}))

    @patch("data_provider.DataProvider.get_fiscalcode_list_from_Anagrafica")
    def test_filter_fiscalcodes_dataframe_str(self, mock_method):
        # Creo lista di codici fiscali fittizzi, solo i primi 2 corrispondono
        mocked_list = ['08587760961', '02538160033', 
                        '10536370017', 'MRCNTN63H03G942C']
        mock_method.return_value = mocked_list

        # Creo DataProvider di Test
        data = {
            'col1': ['08587760961', '02538160033', '05903120631', '02643150168'],
            'col2': ['UD', 'O', 'P', 'TS']
        }
        df = pd.DataFrame(data)
        col_types = {0: 'object', 1: 'object'}
        col_constraints = {0: True, 1: False}
        dp = DataProvider(df, col_types, col_constraints)

        # Richiamo il metodo da testare inplace
        dp.filter_fiscalcodes_dataframe('col1', inplace=True)

        # Richiamo il metodo da testare con return value
        new_df = dp.filter_fiscalcodes_dataframe('col1', inplace=False)

        # Mi assicuro che il metodo mockato venga chiamato
        mock_method.assert_called()

        # Effettuo il test
        pd.testing.assert_frame_equal(dp.df, pd.DataFrame(
            {'col1': ['08587760961', '02538160033'], 'col2': ['UD', 'O']}))
        pd.testing.assert_frame_equal(new_df, pd.DataFrame(
            {'col1': ['08587760961', '02538160033'], 'col2': ['UD', 'O']}))
            
    def test_get_column_constraints_is_respected(self):
        from data_provider import DataProvider
        # Test su colonna di interi
        self.assertEqual(
            2, self.dp.get_column_constraints_is_respected().sum())

        # Test su una colonna di stringhe
        # Creo istanza di Data Provider
        data = {
            # duplicato il secondo valore
            'col1': ['222365896', '522559845', '333652214', '522559845'],
            'col2': ['UD', '   O', 'P   ', '   TS    ']
        }
        df = pd.DataFrame(data)
        col_types = {0: 'object', 1: 'object'}
        col_constraints = {0: True, 1: False}
        dp = DataProvider(df, col_types, col_constraints)
        # Test valore corrispondente
        self.assertEqual(1, dp.get_column_constraints_is_respected().sum(),
                         "E' presente un duplicato nella colonna!")
        # Test valore non corrispondente
        self.assertNotEqual(0, dp.get_column_constraints_is_respected().sum(),
                            "E' presente un duplicato nella colonna!")
