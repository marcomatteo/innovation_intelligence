import unittest as test
import pandas as pd
import numpy as np
from datetime import datetime

from data_providers import (
        formatFiscalcodeColumn, formatFiscalcode,
        getColumnNames, getColumnsTypes, 
        getColumnsMaxLength, getColumnNullables,
        getNumerateDictFromList
    )
from data_providers.dataProviderUtil import (
    getTrimmedLength, getMaxLength, ColumnHaveNullValues
)


class Test_DataProviderUtil(test.TestCase):

    def test_getNumerateDictFromList_right(self):
        default_dict = {
            0: 'valore0',
            1: '2',
            2: 'True',
            3: '0.23'
        }

        test_list = ['valore0', '2', 'True', '0.23']

        self.assertDictEqual(
            default_dict,
            getNumerateDictFromList(test_list),
            "Wrong dictionary conversion from list"
        )
    
    def test_formatFiscalcode_right(self):
        fiscalcode_array = [ 
            1, 12, 123, 
            1234, 12345, 123456, 
            1234567, 12345678, 123456789,
            1234567890, 12345678901
        ]
        formatted_fiscalcode_array = [
            '00000000001', 
            '00000000012', 
            '00000000123', 
            '00000001234', 
            '00000012345', 
            '00000123456', 
            '00001234567', 
            '00012345678', 
            '00123456789',
            '01234567890', 
            '12345678901'
        ]
        index = np.arange(0, len(fiscalcode_array))
        original_series = pd.Series(
            fiscalcode_array, 
            index
        )
        formatted_series = original_series.map(
            lambda x: formatFiscalcode(x)
        )
        self.assertListEqual(
            formatted_fiscalcode_array,
            formatted_series.values.tolist()
        )

    def test_formatFiscalcodeColumn_right(self):
        fiscalcode_array = [ 
            1, 12, 123, 
            1234, 12345, 123456, 
            1234567, 12345678, 123456789,
            1234567890, 12345678901
        ]
        formatted_fiscalcode_array = [
            '00000000001', 
            '00000000012', 
            '00000000123', 
            '00000001234', 
            '00000012345', 
            '00000123456', 
            '00001234567', 
            '00012345678', 
            '00123456789',
            '01234567890', 
            '12345678901'
        ]
        index = np.arange(0, len(fiscalcode_array))
        original_table = pd.DataFrame(
            fiscalcode_array, 
            index,
            columns=['fiscalcode']
        )
        formatted_table = formatFiscalcodeColumn(
            original_table,
            'fiscalcode'
        )
        self.assertListEqual(
            formatted_fiscalcode_array,
            formatted_table['fiscalcode'].values.tolist()
        )

    def test_getColumnNames_right(self):
        col_names = ['Colonna1', 'Colonna2']
        default_col_names = {0: 'Colonna1', 1: 'Colonna2'}
        
        col1 = np.random.randint(0, 100, 100)
        col2 = np.random.randint(-100, 0, 100)
        cols = dict(zip(col_names, [col1, col2]))
        index = np.arange(0, 100, 1)
        test_df = pd.DataFrame(data=cols, index=index)

        self.assertDictEqual(
            default_col_names,
            getColumnNames(test_df),
            "Error getColumnNames"
        )

    def test_getColumnsTypes_right(self):
        default_numpy_types_list = {
            0: np.dtype('O'), # object type
            1: np.dtype('int64'), # signed integer
            2: np.dtype('float64'), # float
            3: np.dtype('<M8[ns]') # datetime
        }

        datetimes = [
            datetime(2019, 9, 30),
            datetime(2020, 2, 29),
            datetime(2018, 8, 30)
        ]
        test_data = {
            'col0': ['casa', '000342', 'abcABC0123lk#'],
            'col1': [0, 123, 9999999],
            'col2': [0.2, 0.0002, 123.456],
            'col3': [
                np.datetime64(datetimes[0]),
                np.datetime64(datetimes[1]),
                np.datetime64(datetimes[2])
            ]
        }
        test_df = pd.DataFrame(test_data)

        self.assertDictEqual(
            default_numpy_types_list,
            getColumnsTypes(test_df),
            "Error test getColumnsTypes"
        )
    
    def test_getTrimmedLength_int(self):
        default_length = 3
        value = 234
        self.assertEqual(
            default_length,
            getTrimmedLength(value),
            "Integer 234 must have length 3!"
        )

    def test_getTrimmedLength_float(self):
        default_length = 6
        value = 234.02
        self.assertEqual(
            default_length,
            getTrimmedLength(value),
            "Float 234.02 must have length 6!"
        )
    
    def test_getTrimmedLength_string(self):
        default_length = 9
        value = " Ciao ciao "
        self.assertEqual(
            default_length,
            getTrimmedLength(value),
            "String 'Ciao ciao ' must have length 9!"
        )
    
    def test_getTrimmedLength_nan(self):
        value = np.nan
        self.assertFalse(getTrimmedLength(value), "Nan Length must be 0!")
    
    def test_getMaxLength_PositiveIntSeries(self):
        default_length = 3
        series_obj = pd.Series(
            data = np.random.randint(0, 200, size=(100,)),
            index = range(0,100)
        )
        self.assertEqual(
            default_length,
            getMaxLength(series_obj),
            "Positive integer Series from 0 to 200 must have max length 3!"
        )
    
    def test_getMaxLength_NegativeIntSeries(self):
        default_length = 4
        series_obj = pd.Series(
            data = np.random.randint(-200, 0, size=(100,)),
            index = range(0,100)
        )
        self.assertEqual(
            default_length,
            getMaxLength(series_obj),
            "Negative integer Series from -200 to 0 must have max length 4!"
        )
    
    def test_getMaxLength_FloatSeries(self):
        default_length = 5
        series_obj = pd.Series(
            data = np.around((np.random.random_sample((100,)) * 200)), # 0<x<200
            index = range(0,100)
        )
        self.assertEqual(
            default_length,
            getMaxLength(series_obj),
            "Positive float Series from 0 to 200 (123.45) must have max length 5!"
        )
    
    def test_getMaxLength_StringSeries(self):
        default_length = 5
        rand_int_array = np.random.randint(1,6,size=(100,)) # 100 elements from 1 to 5
        sample_string = "a"
        composed_string_list = [
            sample_string * val
            for val in rand_int_array
        ]
        series_obj = pd.Series(
            data = composed_string_list, 
            index = range(0,100)
        )
        self.assertEqual(
            default_length,
            getMaxLength(series_obj),
            "String Series from 'a' to 'aaaaa' must have max length 5!"
        )
    
    def test_getColumnsMaxLength_right(self):
        default_max_length = {
            0: 10, 
            1: 2,
            2: 1,
            3: 0
        }
        test_data = {
            'col1': [
                '    min    ',
                'asdasdasd0',
                '          ciao',
                'ciao          '],
            'col2': ['UD', '   O', 'P   ', '   TS    '],
            'col3': [0, 1, 2, 1],
            'col4': [np.nan] * 4
        }
        test_df = pd.DataFrame(test_data)
        self.assertDictEqual(
            default_max_length,
            getColumnsMaxLength(test_df),
            "Error getColumnsMaxLength"
        )
    
    def test_ColumnHaveNullValues_False(self):
        data = [0,1,2,3,4,5,6,7,8,9]
        test_series = pd.Series(data=data, index=range(0,10))
        self.assertFalse(ColumnHaveNullValues(
            test_series),
            "Column don't have nan values"
        )
    
    def test_ColumnHaveNullValues_True(self):
        data = ['Ciao'] * 5 + [None] + ['casa'] * 4
        test_series = pd.Series(data=data, index=range(0,10))
        self.assertTrue(ColumnHaveNullValues(
            test_series),
            "Column has one nan value"
        )
    
    def test_getColumnNullables(self):
        default_nans = {
            0: False, 
            1: True,
            2: False,
            3: True
        }
        test_data = {
            'col1': [
                '    min    ',
                'asdasdasd0',
                '          ciao',
                'ciao          '],
            'col2': ['UD', '   O', None, '   TS    '],
            'col3': [0, 1, 2, 1],
            'col4': [np.nan] * 4
        }
        test_df = pd.DataFrame(test_data)
        self.assertDictEqual(
            default_nans,
            getColumnNullables(test_df),
            "Column 1 and 3 have nan values"
        )
        

if __name__ == '__main__':
    test.main()