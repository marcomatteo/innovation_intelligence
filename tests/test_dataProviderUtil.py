import unittest as test
import pandas as pd
import numpy as np
from datetime import datetime

from data_providers import (
        formatFiscalcodeColumn, formatFiscalcode,
        getColumnNames, getColumnsTypes, 
        getColumnsMaxLenght, getColumnsNullPresence
    )

class Test_DataProviderUtil(test.TestCase):
    
    def test_formatFiscalcode(self):
        #fiscalcode_array = np.random.randint(1, 99999999, 100)
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

    def test_formatFiscalcodeColumn(self):
        #fiscalcode_array = np.random.randint(1, 99999999, 100)
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

    def test_getColumnNames(self):
        """
        La funzione serve per ottenere una lista \
            contenente le colonne di un DataFrame
        
        Input:
        ------
            df: pd.DataFrame
        
        Output:
        -------
            names_list: list
        """
        col1 = np.random.randint(0, 100, 100)
        col2 = np.random.randint(-100, 0, 100)
        col_names = ['Colonna1', 'Colonna2']
        cols = dict(zip(col_names, [col1, col2]))
        index = np.arange(0, 100, 1)
        df = pd.DataFrame(data=cols, index=index)

        cols_mod = getColumnNames(df)

        self.assertListEqual(
            col_names,
            cols_mod,
            "I nomi delle colonne non corrispondono.\n" \
                + "Colonne originali: {}\n".format(col_names) \
                + "Colonne ottenute: {}".format(cols_mod)
        )

    
    

if __name__ == '__main__':
    test.main()