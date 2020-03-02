"""
21/08/2019

"""

import unittest as test
import pandas as pd
import numpy as np

from data_providers import Accredia

from data_providers import \
    formatFiscalcodeColumn, formatFiscalcode, \
    getColumnNames, getColumnsTypes, \
    getColumnsMaxLenght, getColumnsNullPresence

# DB_INTERFACE
#from innovation_intelligence.db_interface.i2fvg import I2FVG

class Test_Accredia(test.TestCase):
    # DB_INTERFACE
    table_name = 'DATA_Certificazione'
    # Formato del file fonte
    source_default_type = "csv"
    source_default_sep = '|'
    # Elenco delle colonne previste
    table_columns = [
        'fiscalcode',           # Primary key
        'annomese',             # 
        'regulation',           # 
        'id_istat_province',    # Primary key
        'istat_province_prcode' # 
    ]
    # Chiavi primarie - valori univoci
    df_keys = [0, 4]
    # Definizione tipi delle colonne
    columns_types = [
        np.dtype('O'),
        np.dtype('int64'),
        np.dtype('O'),
        np.dtype('int64'),
        np.dtype('O')
    ]
    # Lunghezza max dei campi
    columns_max_lenght = [19, 10, 50, 10, 2]
    # Possono essere Na
    columns_not_null = [True] * 5
    #############################################################
    
    @classmethod
    def setUpClass(cls):
        cls.accredia = Accredia("20200203_accredia.csv")
        #cls.db = I2FVG()
        #cls.info = cls.db.get_stats(cls.table_name)

    # Test estensione del file fonte se csv
    def test_acceptance_fileExtension(self):
        default_type = self.source_default_type
        fileExtension_type = self.accredia.file_ext
        self.assertEqual(
            default_type, 
            fileExtension_type,
            "Data Provider wrong extension. Expected file in {} format".format(default_type)
        )

    def test_acceptance_fileSeparator(self):
        default_separator = self.source_default_sep
        fileSeparator_string = self.accredia.sep
        self.assertEqual(
            default_separator, 
            fileSeparator_string,
            "Data Provider wrong csv separator. Expected a {}".format(default_separator)
        )

    def test_acceptance_columnsNumber(self):
        default_columns_number = len(self.table_columns)
        columns_names_number = len(getColumnNames(self.accredia.df))
        self.assertEqual(
            default_columns_number,
            columns_names_number,
            "Data Provider wrong columns number. Expected {}".format(default_columns_number)
        )

    def test_acceptance_columnsTypes(self):
        default_columns_type = self.columns_types
        columns_types = getColumnsTypes(self.accredia.df)
        self.assertEqual(
            default_columns_type,
            columns_types,
            "Data Provider wrong columns types. Expected {}".format(default_columns_type)
        )

    def test_acceptance_columnsMaxLenght(self):
        default_columns_max_lenght = self.columns_max_lenght
        columns_max_lenght = getColumnsMaxLenght(self.accredia.df)

        # Test through all the columns
        for column_number, max_lenght in enumerate(default_columns_max_lenght):
            # Conditional assertion test
            if columns_max_lenght[column_number] > max_lenght:
                column = self.accredia.df.iloc[:, column_number]
                condition = column > max_lenght
                rows_to_check = column.loc[condition]
                for index, value in rows_to_check.iteritems():
                    # subTest allows no interruption if test fails
                    with self.subTest(max = max_lenght):
                        value_lenght = len(str(value))
                        self.assertGreaterEqual(
                            max_lenght, 
                            value_lenght,
                            "Column {}, row {} has {}".format(
                                column, index, value_lenght
                            )
                        )
    
    def test_acceptance_columnsNotNull(self):
        default_columns_not_null = self.columns_not_null
        default_columns_must_be_not_null = [
            boolean 
            for boolean in default_columns_not_null
            if boolean
        ]
        columns_not_null = getColumnsNullPresence(self.accredia.df)

        # Test through all the columns
        for column_number, _ in enumerate(default_columns_must_be_not_null):
            # Conditional assertion test
            if columns_not_null[column_number] == True:
                column = self.accredia.df.iloc[:, column_number]
                rows_to_check = column.isna()
                for index, value in rows_to_check.iteritems():
                    # subTest allows no interruption if test fails
                    with self.subTest():
                        self.assertTrue(
                            value,
                            "Column {}, row {} has {}".format(
                                column_number, index, value
                            )
                        )
                        
if __name__ == '__main__':
    test.main()