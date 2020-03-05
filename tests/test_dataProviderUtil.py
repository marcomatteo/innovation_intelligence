import unittest as test
import pandas as pd
import numpy as np
from datetime import datetime

from data_providers import (
        formatFiscalcodeColumn, formatFiscalcode,
        getColumnNames, getColumnsTypes, 
        getColumnsMaxLenght, getColumnNullables
    )

class Test_DataProviderUtil(test.TestCase):
    
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
        default_col_name = ['Colonna1', 'Colonna2']
        
        col1 = np.random.randint(0, 100, 100)
        col2 = np.random.randint(-100, 0, 100)
        cols = dict(zip(default_col_name, [col1, col2]))
        index = np.arange(0, 100, 1)
        test_df = pd.DataFrame(data=cols, index=index)

        self.assertListEqual(
            default_col_name,
            getColumnNames(test_df),
            "Error getColumnNames"
        )

    def test_getColumnsTypes_right(self):
        default_numpy_types_list = [
            np.dtype('O'), # object type
            np.dtype('int64'), # signed integer
            np.dtype('float64'), # float
            np.dtype('<M8[ns]') # datetime
        ]

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

        self.assertListEqual(
            default_numpy_types_list,
            getColumnsTypes(test_df),
            "Error test getColumnsTypes"
        )
    
    def test_getColumnsMaxLength_right(self):
        default_max_length = [10, 2, 1, 0]
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
        self.assertListEqual(
            default_max_length,
            getColumnsMaxLenght(test_df),
            "Error getColumnsMaxLenght"
        )
        

if __name__ == '__main__':
    test.main()