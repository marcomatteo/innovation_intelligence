import unittest as test
import pandas as pd
import numpy as np
from datetime import datetime

from data_providers import AnagraficaInfocamere
from data_providers import (
    getColumnNames, getColumnsTypes, 
    getColumnsMaxLenght, getColumnNullables
)
from db_interface import I2FVG
from db_interface import getColumnsInfo, getNumpyTypesConversion

class Test_AnagraficaInfocamere(test.TestCase):
    
    source_default_type = "xlsx"
    source_sheet_name = 'FRIULI anagrafica' # info non rilevante
    db_table_name = "TMP_IC_Anagrafica"

    columns_unique = [0, 1, 4]
    date_format = "%d/%m/%Y"
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.anagrafica = AnagraficaInfocamere("Infocamere_06feb2019bis.xlsx")
        cls.i2fvg = I2FVG()
        cls.db_info = cls.i2fvg.get_stats(cls.db_table_name)
        cls.db_columns_info = getColumnsInfo(cls.db_info, slice(0,-2))
        cls.db_column_dates = [
            idx 
            for idx, typ in enumerate(cls.db_columns_info.types) 
            if typ is datetime.date
        ]

    def test_acceptance_fileExtension(self):
        default_type = self.source_default_type
        test_fileExtension_type = self.anagrafica.file_ext
        self.assertEqual(
            default_type, 
            test_fileExtension_type,
            "Data Provider wrong extension. Expected file in {} format".format(default_type)
        )

    def test_acceptance_columnsNumber(self):
        default_columns_number = len(self.db_columns_info.names)
        test_columns_names_number = len(getColumnNames(self.anagrafica.df))
        self.assertEqual(
            default_columns_number,
            test_columns_names_number,
            "Data Provider wrong columns number. Expected {}".format(default_columns_number)    
        )

    def test_acceptance_columnsTypes(self):
        default_columns_type = getNumpyTypesConversion(self.db_columns_info.types)
        test_columns_types = getColumnsTypes(self.anagrafica.df)
        self.assertEqual(
            default_columns_type,
            test_columns_types,
            "\nData Provider wrong columns types.\n" + \
            "Differences: \n{}".format(
                {
                    x: y
                    for x,y in zip(
                        default_columns_type, test_columns_types
                    )
                }
            )
        )

    def test_acceptance_columnsMaxLenght(self):
        
        def trimmedLength(x) -> int:
            s = str(x).strip()
            return len(s)

        default_columns_max_lenght = self.db_columns_info.lengths
        test_columns_max_lenght = getColumnsMaxLenght(self.anagrafica.df)

        # Test through all the columns
        for column_number, max_lenght in enumerate(default_columns_max_lenght):
            # If not Null
            if max_lenght:
                # Conditional assertion test
                if test_columns_max_lenght[column_number] > max_lenght:
                    column = self.anagrafica.df.iloc[:, column_number].map(
                        lambda x: trimmedLength(x))
                    condition = column > max_lenght
                    rows_to_check = column.loc[condition]
                    #TODO: sostituire iteritems() con metodo vettorizzato
                    for index, value in rows_to_check.iteritems():
                        # subTest allows no interruption if test fails
                        with self.subTest(max = max_lenght):
                            value_lenght = len(str(value).strip())
                            self.assertGreaterEqual(
                                max_lenght, 
                                value_lenght,
                                "Column {}, row {} has {}".format(
                                    column_number, index, value_lenght
                                )
                            )
    
    def test_acceptance_columnsNullable(self):
        default_columns_nullables = self.db_columns_info.nullables
        test_columns_nullables = getColumnNullables(self.anagrafica.df)

        # Iterazione di tutte le colonne
        for column_number, _ in enumerate(default_columns_nullables):
            # Effettuo il controllo solo se False -> non può essere nullable (null)
            if test_columns_nullables[column_number] == False:
                # Seleziono la colonna
                column = self.anagrafica.df.iloc[:, column_number]
                # Boolean vector per selezionare i campi NA (null)
                col_to_check = column.isna()
                # Lista delle posizioni nel vettore in cui mancano i valori
                missing_list = self.anagrafica.df.loc[col_to_check].index.values.tolist()
                with self.subTest():
                    self.assertListEqual(
                        [], # Empty list
                        missing_list,
                        "Trovati valori mancanti!\n" + \
                        "Colonna n. {}\n".format(column_number) + \
                        "Indici: {}".format(missing_list) 
                    )
                        
    def test_acceptance_columnsDateFormat(self):

        def dateTextIsValid(text: str, date_format: str) -> bool:
            try:
                datetime.strptime(text, date_format)
            except ValueError:
                return False
            return True

        for column in self.db_column_dates:
            test_column_series = self.anagrafica.df.iloc[:,column]
            # Test each row
            for index, value in test_column_series.iteritems():
                true_value = dateTextIsValid(value, self.date_format)
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