from unittest import TestCase
from unittest.mock import call, patch

import pandas as pd
import numpy as np
import datetime

from data_provider import DataProvider


class Test_DataProvider(TestCase):

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

    @patch("data_provider.DataProvider.get_casted_dataframe")
    def test_get_column_types(self, mock_method):
        mock_method.return_value = pd.DataFrame({
            'col1': ['    min    ', 'asdasdasd0', '          ciao', 'ciao          '],
            'col2': ['UD', '   O', 'P   ', '   TS    '],
            'col3': [0, 1, 1, 1],
            'col4': ([np.nan] * 3) + [0.24],
            'col5': pd.date_range(start=datetime.datetime.today(), periods=4)
        })

        self.assertEqual(self.dp.get_column_types(), [np.dtype('O'),
                                                      np.dtype('O'),
                                                      np.dtype('int64'),
                                                      np.dtype('float64'),
                                                      np.dtype('<M8[ns]')])

    @patch("data_provider.DataProvider.get_column_max_length_is_respected")
    def test_get_column_max_length(self, mock_method):
        mock_method.side_effect = [10, 2, 1, 4, 26]
        max_length = self.dp.get_columns_max_length()
        self.assertEqual(max_length, [10, 2, 1, 4, 26])

    def test_get_column_nullables(self):
        self.assertEqual(self.dp.get_column_nullables(), [False, False, False, True, False])

    def test_get_casted_column_for_type_object(self):
        s = pd.Series(['ciao', '2', '12/05/2020', '4.563'], dtype='object')
        casted_s = DataProvider.get_casted_column_for_type(s, 'object')
        pd.testing.assert_frame_equal(casted_s, pd.DataFrame(
            ['ciao', '2', '12/05/2020', '4.563']))
        self.assertEqual(casted_s.dtypes.tolist(), [np.dtype('O')])

    def test_get_casted_column_for_type_int(self):
        s = pd.Series(['1', '2', '3', '4'], dtype='object')
        casted_s = DataProvider.get_casted_column_for_type(s, 'int')
        pd.testing.assert_frame_equal(casted_s, pd.DataFrame([1, 2, 3, 4]))
        self.assertEqual(casted_s.dtypes.tolist(), [np.dtype('int64')])

    def test_get_casted_column_for_type_float(self):
        s = pd.Series(['1.5', '2.5', '3.5', '4.5'], dtype='object')
        casted_s = DataProvider.get_casted_column_for_type(s, 'float')
        pd.testing.assert_frame_equal(
            casted_s, pd.DataFrame([1.5, 2.5, 3.5, 4.5]))
        self.assertEqual(casted_s.dtypes.tolist(), [np.dtype('float64')])

    def test_get_casted_column_for_type_date(self):
        s = pd.Series(['05/11/2020', '05/12/2020', '05/13/2020',
                       '05/14/2020'], dtype='object')
        casted_s = DataProvider.get_casted_column_for_type(s, 'date')

        date_series = pd.date_range(start='05/11/2020', periods=4)
        pd.testing.assert_frame_equal(casted_s, pd.DataFrame(date_series))
        self.assertEqual(casted_s.dtypes.tolist(), [np.dtype('<M8[ns]')])

    @patch('data_provider.DataProvider.get_casted_column_for_type')
    def test_get_casted_dataframe(self, mock_method):
        date_column = pd.date_range(start=datetime.datetime.today(), periods=4)
        mock_method.side_effect = [
            pd.DataFrame(['    min    ', 'asdasdasd0',
                          '          ciao', 'ciao          '], dtype='object'),
            pd.DataFrame(['UD', '   O', 'P   ', '   TS    '], dtype='object'),
            pd.DataFrame([0, 1, 1, 1]),
            pd.DataFrame((([np.nan] * 3) + [0.24]), dtype='float64'),
            pd.DataFrame(date_column)
        ]

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
        test_dp = DataProvider(
            df=df,
            column_types={0: 'object', 1: 'object',
                          2: 'int', 3: 'float', 4: 'date'},
            column_constraints={0: False, 1: False, 2: True, 3: False, 4: False})

        # Effettuo il casting
        casted_df = test_dp.get_casted_dataframe()

        self.assertEqual(casted_df.dtypes.tolist(),
                         [np.dtype('O'), np.dtype('O'),
                          np.dtype('int64'), np.dtype('float64'), np.dtype('<M8[ns]')])

    def test_get_trimmed_length(self):
        self.assertEqual(self.dp.get_trimmed_length(234), 3)

        self.assertEqual(self.dp.get_trimmed_length(-234), 4)

        self.assertEqual(self.dp.get_trimmed_length(234.02), 6)

        self.assertEqual(self.dp.get_trimmed_length(-234.02), 7)

        self.assertEqual(self.dp.get_trimmed_length(" Ciao ciao "), 9)

        self.assertEqual(self.dp.get_trimmed_length(" Ciao ciao"), 9)

        self.assertEqual(self.dp.get_trimmed_length("Ciao ciao "), 9)

        self.assertFalse(self.dp.get_trimmed_length(np.nan))

        self.assertFalse(self.dp.get_trimmed_length(pd.NaT))

    def test_catch_null_length_isnan(self):
        self.assertTrue(self.dp.catch_null_length(np.isnan, np.nan))
        self.assertTrue(self.dp.catch_null_length(pd.isnull, pd.NaT))
        self.assertTrue(self.dp.catch_null_length(np.isnat,
                                                  np.datetime64("NaT")))

    @patch("data_provider.DataProvider.get_trimmed_length")
    def test_get_column_max_length_is_respected_int_positives(self, mock_method):
        mock_method.side_effect = [1, 3, 4, 1]
        s = pd.Series([1, 100, 2589, 3])

        s_max_length = DataProvider.get_column_max_length_is_respected(s)

        calls = [call(1), call(100), call(2589), call(3)]
        mock_method.assert_has_calls(calls)

        self.assertEqual(s_max_length, 4)

    @patch("data_provider.DataProvider.get_trimmed_length")
    def test_get_column_max_length_is_respected_int_negatives(self, mock_method):
        mock_method.side_effect = [2, 4, 5, 2]
        s = pd.Series([-1, -100, -2589, -3])

        s_max_length = DataProvider.get_column_max_length_is_respected(s)

        calls = [call(-1), call(-100), call(-2589), call(-3)]
        mock_method.assert_has_calls(calls)

        self.assertEqual(s_max_length, 5)

    @patch("data_provider.DataProvider.get_trimmed_length")
    def test_get_column_max_length_is_respected_float_positives(self, mock_method):
        mock_method.side_effect = [3, 5, 6, 4]
        s = pd.Series([1.5, 100.5, 2589.5, 3.26])

        s_max_length = DataProvider.get_column_max_length_is_respected(s)

        calls = [call(1.5), call(100.5), call(2589.5), call(3.26)]
        mock_method.assert_has_calls(calls)

        self.assertEqual(s_max_length, 6)

    @patch("data_provider.DataProvider.get_trimmed_length")
    def test_get_column_max_length_is_respected_float_negatives(self, mock_method):
        mock_method.side_effect = [4, 6, 7, 5]
        s = pd.Series([-1.5, -100.5, -2589.5, -3.26])

        s_max_length = DataProvider.get_column_max_length_is_respected(s)

        calls = [call(-1.5), call(-100.5), call(-2589.5), call(-3.26)]
        mock_method.assert_has_calls(calls)

        self.assertEqual(s_max_length, 7)

    @patch("data_provider.DataProvider.get_trimmed_length")
    def test_get_column_max_length_is_respected_strings(self, mock_method):
        mock_method.side_effect = [4, 6, 7, 5]
        s = pd.Series(['ciao', 'ciao o', 'ciao oo', ' aciao '])

        s_max_length = DataProvider.get_column_max_length_is_respected(s)

        calls = [call('ciao'), call('ciao o'),
                 call('ciao oo'), call(' aciao ')]
        mock_method.assert_has_calls(calls)

        self.assertEqual(s_max_length, 7)

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

    def test_get_column_constraints_is_respected_setup(self):
        duplicated_values = self.dp.get_column_constraints_is_respected()
        # Sono segnati come duplicati gli le ultime due righe
        pd.testing.assert_series_equal(duplicated_values, pd.Series([False, False, True, True]))
        self.assertEqual(duplicated_values.sum(), 2)

    def test_get_column_constraints_is_respected_strings(self):
        # Creo istanza di Data Provider
        data = {
            # duplicando l'ultimo valore della prima colonna
            'col1': ['222365896', '522559845', '333652214', '522559845'],
            'col2': ['UD', '   O', 'P   ', '   TS    ']
        }
        df = pd.DataFrame(data)
        col_types = {0: 'object', 1: 'object'}
        col_constraints = {0: True, 1: False}
        dp = DataProvider(df, col_types, col_constraints)

        # Test valore corrispondente
        duplicated_values = dp.get_column_constraints_is_respected()
        pd.testing.assert_series_equal(duplicated_values, pd.Series([False, False, False, True]))
        self.assertEqual(duplicated_values.sum(), 1)

    def test_get_column_constraints_is_respected_multicolumn(self):
       # Creo istanza di Data Provider
        data = {
            'col1': ['222365896', '522559845', '522559845', '522559845'],
            'col2': ['UD', 'GO', 'PN', 'GO'],
            'col3': [1, 2, 3, 4]
        }
        df = pd.DataFrame(data)
        col_types = {0: 'object', 1: 'object', 2: 'int'}
        col_constraints = {0: True, 1: True, 2: False}
        dp = DataProvider(df, col_types, col_constraints)

        # Test valore corrispondente
        duplicated_values = dp.get_column_constraints_is_respected()
        pd.testing.assert_series_equal(duplicated_values, pd.Series([False, False, False, True]))
        self.assertEqual(duplicated_values.sum(), 1)

    def test_get_column_constraints_is_respected_NotImplemented(self):
        # Creo istanza di Data Provider
        data = {
            # duplicando l'ultimo valore della prima colonna
            'col1': ['222365896', '522559845', '333652214', '522559845'],
            'col2': ['UD', '   O', 'P   ', '   TS    ']
        }
        df = pd.DataFrame(data)
        col_types = {0: 'object', 1: 'object'}
        dp = DataProvider(df, col_types, column_constraints=NotImplemented)

        # Test valore corrispondente
        duplicated_values = dp.get_column_constraints_is_respected()
        pd.testing.assert_series_equal(duplicated_values, pd.Series([], dtype='object'))

if __name__ == '__main__':
    from unittest import main
    main(verbosity=2)
