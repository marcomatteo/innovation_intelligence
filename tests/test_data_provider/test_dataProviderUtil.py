import unittest as test
import pandas as pd
import numpy as np
import logging

from datetime import datetime

from data_providers import (
        formatFiscalcodeColumn, formatFiscalcode,
        getColumnNames, getColumnsTypes, 
        getColumnsMaxLength, getColumnNullables,
        getNumerateDictFromList, getBoolSeriesForDateChecking,
        getColumnTest, getTableTest,
        getTrimmedLength, getMaxLength, ColumnHaveNullValues,
        isValidDateFormat
    )


from tests import LogCaptureRunner, BaseTestCase

class Test_DataProviderUtil(test.TestCase):

    def test_getNumerateDictFromList_right(self):
        test_list = ['valore0', '2', 'True', '0.23']
        self.assertDictEqual(
            getNumerateDictFromList(test_list),
            {0: 'valore0', 1: '2', 2: 'True', 3: '0.23'},
            "Wrong dictionary conversion from list"
        )
    
    def test_formatFiscalcode_right(self):
        fiscalcode_array = [ 
            1, 12, 123, 
            1234, 12345, 123456, 
            1234567, 12345678, 123456789,
            1234567890, 12345678901
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
            formatted_series.values.tolist(), [
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
        )

    def test_formatFiscalcodeColumn_right(self):
        fiscalcode_array = [ 
            1, 12, 123, 
            1234, 12345, 123456, 
            1234567, 12345678, 123456789,
            1234567890, 12345678901
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
            formatted_table['fiscalcode'].values.tolist(),[
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
        )

    def test_getColumnNames_right(self):
        col_names = ['Colonna1', 'Colonna2']
        col1 = np.random.randint(0, 100, 100)
        col2 = np.random.randint(-100, 0, 100)
        cols = dict(zip(col_names, [col1, col2]))
        index = np.arange(0, 100, 1)
        test_df = pd.DataFrame(data=cols, index=index)

        self.assertDictEqual(
            getColumnNames(test_df),
            {0: 'Colonna1', 1: 'Colonna2'},
            "Error getColumnNames"
        )

    def test_getColumnsTypes_right(self):
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
            getColumnsTypes(test_df), {
                0: np.dtype('O'), # object type
                1: np.dtype('int64'), # signed integer
                2: np.dtype('float64'), # float
                3: np.dtype('<M8[ns]') # datetime
            },
            "Error test getColumnsTypes"
        )
    
    def test_getTrimmedLength_int(self):
        value = 234
        self.assertEqual(
            getTrimmedLength(value), 3,
            "Integer 234 must have length 3!"
        )

    def test_getTrimmedLength_float(self):
        value = 234.02
        self.assertEqual(
            getTrimmedLength(value), 6,
            "Float 234.02 must have length 6!"
        )
    
    def test_getTrimmedLength_string(self):
        value = " Ciao ciao "
        self.assertEqual(
            getTrimmedLength(value), 9,
            "String 'Ciao ciao ' must have length 9!"
        )
    
    def test_getTrimmedLength_nan(self):
        value = np.nan
        self.assertFalse(getTrimmedLength(value), "Nan Length must be 0!")
    
    def test_getMaxLength_PositiveIntSeries(self):
        series_obj = pd.Series(
            data = np.random.randint(0, 200, size=(100,)),
            index = range(0,100)
        )
        self.assertEqual(
            getMaxLength(series_obj), 3,
            "Positive integer Series from 0 to 200 must have max length 3!"
        )
    
    def test_getMaxLength_NegativeIntSeries(self):
        series_obj = pd.Series(
            data = np.random.randint(-200, 0, size=(100,)),
            index = range(0,100)
        )
        self.assertEqual(
            getMaxLength(series_obj), 4,
            "Negative integer Series from -200 to 0 must have max length 4!"
        )
    
    def test_getMaxLength_FloatSeries(self):
        series_obj = pd.Series(
            data = np.around((np.random.random_sample((100,)) * 200)), # 0<x<200
            index = range(0,100)
        )
        self.assertEqual(
            getMaxLength(series_obj), 5,
            "Positive float Series from 0 to 200 (123.45) must have max length 5!"
        )
    
    def test_getMaxLength_StringSeries(self):
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
            getMaxLength(series_obj), 5,
            "String Series from 'a' to 'aaaaa' must have max length 5!"
        )
    
    def test_getColumnsMaxLength_right(self):
        test_data = {
            'col1': ['    min    ', 'asdasdasd0',
                    '          ciao', 'ciao          '],
            'col2': ['UD', '   O', 'P   ', '   TS    '],
            'col3': [0, 1, 2, 1],
            'col4': [np.nan] * 4
        }
        test_df = pd.DataFrame(test_data)
        self.assertDictEqual(
            getColumnsMaxLength(test_df),
            { 0: 10, 1: 2, 2: 1, 3: 0 },
            "Error getColumnsMaxLength"
        )
    
    def test_ColumnHaveNullValues_False(self):
        data = [0,1,2,3,4,5,6,7,8,9]
        test_series = pd.Series(data=data, index=range(0,10))
        self.assertFalse(
            ColumnHaveNullValues(test_series),
            "Column don't have nan values"
        )
    
    def test_ColumnHaveNullValues_True(self):
        data = ['Ciao'] * 5 + [None] + ['casa'] * 4
        test_series = pd.Series(data=data, index=range(0,10))
        self.assertTrue(
            ColumnHaveNullValues(test_series),
            "Column has one nan value"
        )
    
    def test_getColumnNullables(self):
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
            getColumnNullables(test_df),
            { 0: False,  1: True, 2: False, 3: True },
            "Column 1 and 3 have nan values"
        )
        
    # =======================| Date tests |=======================
    def test_isValidDateFormat_string_right(self):
        dt = "31/01/2020"
        self.assertTrue(
            isValidDateFormat(dt, "%d/%m/%Y"), 
            "String '31/01/2020' must be True")

    def test_isValidDateFormat_nan_right(self):
        dt = np.nan
        self.assertTrue(
            isValidDateFormat(dt, "%d/%m/%Y"), 
            "String 'nan' must be True")
    
    def test_isValidDateFormat_string_wrong_monthFirst(self):
        dt = "01/31/2020"
        self.assertFalse(
            isValidDateFormat(dt, "%d/%m/%Y"), 
            "String '01/31/2020' must be False")
    
    def test_isValidDateFormat_string_wrong_yearFirst(self):
        dt = "2020/01/31"
        self.assertFalse(
            isValidDateFormat(dt, "%d/%m/%Y"), 
            "String '2020/01/31' must be False")

    def test_isValidDateFormat_string_wrong_differentFormat(self):
        dt = "31-01-2020"
        self.assertFalse(
            isValidDateFormat(dt, "%d/%m/%Y"), 
            "String '31-01-2020' must be False")

    def test_isValidDateFormat_string_wrong_differentFormat_extended(self):
        dt = "2020-01-31 00:00:00"
        self.assertFalse(
            isValidDateFormat(dt, "%d/%m/%Y"), 
            "String '2020-01-31 00:00:00' must be False")

    def test_isValidDateFormat_date_right(self):
        dt_str = "31/01/2020"
        dt_date = datetime.strptime(dt_str, "%d/%m/%Y")
        self.assertTrue(
            isValidDateFormat(dt_date, "%d/%m/%Y"), 
            "Date '31/01/2020' must be True")

    @test.skip("Datetime is not ready for checking")
    def test_isValidDateFormat_date_wrongFormat(self):
        #TODO: trovare un modo per convertire date (con format diverso)
        dt_str = "01-31-2020"
        dt_date = datetime.strptime(dt_str, "%m-%d-%Y")
        self.assertFalse(
            isValidDateFormat(dt_date, "%d/%m/%Y"), 
            "datetime from format '%m-%d-%Y' ('01-31-2020') must be False")

    def test_getColumnTest_Date_right(self):
        data = [
            "07/06/2020",
            "30/11/2019",
            "01/01/1992"
        ]
        s = pd.Series(data, index=range(len(data)))
        self.assertTrue(
            getColumnTest(s, isValidDateFormat, "%d/%m/%Y").all(),
            "All is a valid date"
        )
    
    def test_getColumnTest_Date_right_withBlanks(self):
        data = [
            "   07/06/2020    ",
            "   30/11/2019",
            "01/01/1992       "
        ]
        s = pd.Series(data, index=range(len(data)))
        self.assertTrue(
            getColumnTest(s, isValidDateFormat, "%d/%m/%Y").all(),
            "All is a valid date even with blanks (not trimmed yet)"
        )

    def test_getColumnTest_Date_right_withNan(self):
        data = [
            np.nan,
            "30/11/2019",
            np.nan
        ]
        s = pd.Series(data, index=range(len(data)))
        self.assertTrue(
            getColumnTest(s, isValidDateFormat, "%d/%m/%Y").all(),
            "Even with missing values, the Series is all right"
        )
    
    def test_getColumnTest_Date_right_allNan(self):
        data = [
            np.nan,
            np.nan,
            np.nan
        ]
        s = pd.Series(data, index=range(len(data)))
        self.assertTrue(
            getColumnTest(s, isValidDateFormat, "%d/%m/%Y").all(),
            "Even with all missing values, the Series is all right"
        )
    
    def test_getColumnTest_Date_wrong_all(self):
        data = [
            "09/16/2020",
            "04/13/2019",
            "06/30/1992"
        ]
        s = pd.Series(data, index=range(len(data)))
        self.assertFalse(
            getColumnTest(s, isValidDateFormat, "%d/%m/%Y").all(),
            "All is an invalid date"
        )

    def test_getColumnTest_Date_wrong_one(self):
        data = [
            "09/02/2020",
            "04/01/2019",
            "06/30/1992"
        ]
        s = pd.Series(data, index=range(len(data)))
        self.assertFalse(
            getColumnTest(s, isValidDateFormat, "%d/%m/%Y").all(),
            "One is an invalid date, so must be False"
        )

    def test_getColumnTest_Date_wrong_allFormat(self):
        data = [
            "07-06-2020",
            "30-11-2019",
            "01-01-1992"
        ]
        s = pd.Series(data, index=range(len(data)))
        self.assertFalse(
            getColumnTest(s, isValidDateFormat, "%d/%m/%Y").all(),
            "All is an invalid date by format '%d-%m-%Y'"
        )

    def test_getColumnTest_Date_wrong_oneFormat(self):
        data = [
            "07-06-2020",
            "30/11/2019",
            "01/01/1992"
        ]
        s = pd.Series(data, index=range(len(data)))
        self.assertFalse(
            getColumnTest(s, isValidDateFormat, "%d/%m/%Y").all(),
            "One is an invalid date by format '%d-%m-%Y', so must be False"
        )

    def test_getTableTest_Date_ok(self):
        col1 = [
            "07/06/2020",
            "30/11/2019",
            "01/01/1992"
        ]
        col2 = [
            "   07/06/2020    ",
            "   30/11/2019",
            "01/01/1992       "
        ]
        col3 = [
            np.nan,
            "30/11/2019",
            np.nan
        ]
        col4 = [
            np.nan,
            np.nan,
            np.nan
        ]
        cols = {
            'c1': col1,
            'c2': col2,
            'c3': col3,
            'c4': col4
        }
        df = pd.DataFrame(cols, index=range(3))
        self.assertTrue(
            getTableTest(df, isValidDateFormat, "%d/%m/%Y").all(),
            "All the columns have right formatting date ('%d-%m-%Y')," \
                + " so must be False"
        )