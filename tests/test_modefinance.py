"""
23/10/2019

Classe di test per modefinance

Innovation Intelligence in Python
Marco Matteo Buzzulini
"""

import unittest as test
import pandas as pd
import numpy as np
from datetime import datetime

from data_providers import Modefinance
from data_providers import \
    formatFiscalcodeColumn, formatFiscalcode, \
    getColumnNames, getColumnsTypes, \
    getColumnsMaxLenght, getColumnsNullPresence

class Test_Modefinance(test.TestCase):
    # PARAMETRI:
    # -----------
    # Formato del file fonte
    source_default_type = "csv"
    source_default_sep = ';'
    table_columns = [
        'fiscal_code',     # Primary key
        'final_rank',       
        'evaluation_date', # Primary key, date
        'is_consolidated',  
    ]
    # Definizione tipi delle colonne
    columns_types = [
        np.dtype('O'), 
        np.dtype('int64'),  
        np.dtype('O'), 
        np.dtype('bool')
    ]
    # Lunghezza max dei campi
    columns_max_lenght = [19, 2, 10, 5]
    # Possono essere Na
    columns_not_null = [True] * 4    
    # Chiavi primarie - valori univoci
    columns_unique = [0, 2]
    # Campo/i data
    columns_is_date = [2]
    # Formato data
    modefinance_date_format = "%d/%m/%Y"
    
    # METODI:
    # -----------
    @classmethod
    def setUpClass(cls):
        cls.modefinance = Modefinance("MFSourceSample_test.csv")

    def test_acceptance_fileExtension(self):
        default_type = self.source_default_type
        fileExtension_type = self.modefinance.file_ext
        self.assertEqual(
            default_type, 
            fileExtension_type,
            "Data Provider wrong extension. Expected file in {} format".format(default_type)
        )

    def test_acceptance_fileSeparator(self):
        default_separator = self.source_default_sep
        fileSeparator_string = self.modefinance.sep
        self.assertEqual(
            default_separator, 
            fileSeparator_string,
            "Data Provider wrong csv separator. Expected a {}".format(default_separator)
        )

    def test_acceptance_columnsNumber(self):
        default_columns_number = len(self.table_columns)
        columns_names_number = len(getColumnNames(self.modefinance.df))
        self.assertEqual(
            default_columns_number,
            columns_names_number,
            "Data Provider wrong columns number. Expected {}".format(default_columns_number)    
        )

    def test_acceptance_columnsTypes(self):
        default_columns_type = self.columns_types
        columns_types = getColumnsTypes(self.modefinance.df)
        self.assertEqual(
            default_columns_type,
            columns_types,
            "Data Provider wrong columns types. Expected {}".format(default_columns_type)
        )
    def test_acceptance_columnsMaxLenght(self):
        default_columns_max_lenght = self.columns_max_lenght
        columns_max_lenght = getColumnsMaxLenght(self.modefinance.df)

        # Test through all the columns
        for column_number, max_lenght in enumerate(default_columns_max_lenght):
            # Conditional assertion test
            if columns_max_lenght[column_number] > max_lenght:
                column = self.modefinance.df.iloc[:, column_number]
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
        columns_has_null = getColumnsNullPresence(self.modefinance.df)

        # Test through all the columns
        for column_number, _ in enumerate(default_columns_must_be_not_null):
            # Conditional assertion test
            if columns_has_null[column_number] == True:
                column = self.modefinance.df.iloc[:, column_number]
                rows_to_check = column.isna()
                for index, value in rows_to_check.iteritems():
                    # subTest allows no interruption if test fails
                    with self.subTest():
                        self.assertTrue(
                            value,
                            "Column {} has missing value ".format(column_number) + \
                            "in row {} :\n{}".format(
                                index, self.modefinance.df.loc[index]
                            )
                        )
                        
    def test_acceptance_finalRankValues(self):
        """
        Test che la colonna 'final_rank' contenga valori compresi tra 1 e 10
        """
        # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        default_values_list = list(range(1,11))

        for index, value in self.modefinance.df['final_rank'].items():
            cond = value in default_values_list
            with self.subTest("Controllo se il rating è valido -> compreso tra 1 e 10"):
                self.assertTrue(
                    cond,
                    "Rating {} non valido in index {}".format(
                        value, index
                    )
                )
            


    def test_acceptance_columnsDateFormat(self):

        def dateTextIsValid(text: str, date_format: str) -> bool:
            try:
                datetime.strptime(text, date_format)
            except ValueError:
                return False
            return True

        for column in self.columns_is_date:
            column_series = self.modefinance.df.iloc[:,column]
            # Test each row
            for index, value in column_series.iteritems():
                true_value = dateTextIsValid(value, self.modefinance_date_format)
                # subTest allows no interruption if test fails
                with self.subTest():
                    self.assertTrue(
                        true_value,
                        "Column {}, row {} has {} while the data format should be {}".format(
                            column,
                            index,
                            value,
                            pd.to_datetime(value, dayfirst=True)
                        )
                    )
        
if __name__ == '__main__':
    test.main()