import unittest as test
import pandas as pd
import numpy as np
from datetime import datetime

from data_providers import AnagraficaInfocamere
from data_providers import (
        formatFiscalcodeColumn, formatFiscalcode, 
        getColumnNames, getColumnsTypes, 
        getColumnsMaxLenght, getColumnsNullPresence 
    )
from db_interface import I2FVG

class Test_AnagraficaInfocamere(test.TestCase):
    # PARAMETRI:
    # -----------
    # Formato del file fonte
    source_default_type = "xlsx"
    source_sheet_name = 'FRIULI anagrafica'
    db_table_name = "TMP_IC_Anagrafica"
    
    table_columns = [
        'codice_fiscale',     
        'provincia',
        'regimp',
        'rea',
        'sedeul',
        'albo',
        'sezioni',
        'naturagiuridica',
        'naturagiuridica_desc',
        'tipoimpresa',
        'iscr_ri',
        'iscr_rd',
        'iscr_aa',
        'aperturaul',
        'cancellazione',
        'inizioattivita',
        'cessazione',
        'fallimento',
        'liquidazione',
        'denominazione',
        'indirizzo',
        'strada',
        'cap',
        'comune',
        'frazione',
        'altreindicazioni',
        'aa_add',
        'ind',
        'dip',
        'partitaiva',
        'telefono',
        'capitale',
        'attivita',
        'valuta',
        'statoimpresa',
        'tiposede_ul1',
        'tiposede_ul2',
        'tiposede_ul3',
        'tiposede_ul4',
        'tiposede_ul5',
        'sedeestero',
        'ul_estero'
        'impresainnovativa',
        'startup',
        'impresafemminile',
        'impresagiovane',
        'impresastraniera',
        'pec']
    # Definizione tipi delle colonne
    columns_types = [
        object,
        object,
        object,
        object,
        object,
        object,
        object,
        object,
        object,
    ]

    # Lunghezza max dei campi
    columns_max_lenght = [
        11,
        2,
        20,
        10,
        10,
        20,
        10,
        2,
        255,
        50,
        # 9 date da inserire, TODO: controllare il formato,
        255,
        100,
        20,
        5,
        100,
        100,
        255,
        # Intero?
        10,
        # Intero?
        11,
        20,
        # Float?
        255,
        30,
        20,
        50,
        50,
        50,
        50,
        50,
        # Bool
        # Bool
        # Bool
        # Bool
        20,
        20,
        20,
        70]

    # Possono essere Na
    columns_not_null = [
        False, 
        False,
        True,
        True,
        False] + ([True] * 43)

    # Chiavi primarie - valori univoci
    columns_unique = [0, 1, 4]

    # Campo/i data
    columns_is_date = list()
    
    # Formato data
    anagrafica_date_format = "%d/%m/%Y" #TODO: da controllare
    
    # METODI:
    # -----------
    @classmethod
    def setUpClass(cls):
        cls.anagrafica = AnagraficaInfocamere("Infocamere_06feb2019bis.xlsx")
        cls.i2fvg = I2FVG()
        cls.db_info = cls.i2fvg.get_stats(cls.db_table_name)
        cls.db_column_names = cls.i2fvg.get_column_names(cls.db_info)[:-1]
        cls.db_column_types = cls.i2fvg.get_column_types(cls.db_info)[:-1]
        cls.db_column_lenght = cls.i2fvg.get_column_length(cls.db_info)[:-1]
        cls.db_column_nullable = cls.i2fvg.get_column_nullable(cls.db_info)[:-1]
        cls.db_column_dates = [idx for idx, typ in enumerate(cls.db_column_types) if typ is datetime.date]

    def test_acceptance_fileExtension(self):
        default_type = self.source_default_type
        fileExtension_type = self.anagrafica.file_ext
        self.assertEqual(
            default_type, 
            fileExtension_type,
            "Data Provider wrong extension. Expected file in {} format".format(default_type)
        )

    def test_acceptance_columnsNumber(self):
        default_columns_number = len(self.db_column_names)
        columns_names_number = len(getColumnNames(self.anagrafica.df))
        self.assertEqual(
            default_columns_number,
            columns_names_number,
            "Data Provider wrong columns number. Expected {}".format(default_columns_number)    
        )

    def test_acceptance_columnsTypes(self):
        default_columns_type = self.columns_types
        columns_types = getColumnsTypes(self.anagrafica.df)
        self.assertEqual(
            default_columns_type,
            columns_types,
            "Data Provider wrong columns types. Expected {}".format(default_columns_type)
        )

    def test_acceptance_columnsMaxLenght(self):
        default_columns_max_lenght = self.db_column_lenght
        columns_max_lenght = getColumnsMaxLenght(self.anagrafica.df)

        # Test through all the columns
        for column_number, max_lenght in enumerate(default_columns_max_lenght):
            # Conditional assertion test
            if columns_max_lenght[column_number] > max_lenght:
                column = self.anagrafica.df.iloc[:, column_number]
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
    
    def test_acceptance_columnsNullable(self):
        default_columns_not_null = self.db_column_nullable
        default_columns_must_be_not_null = [
            boolean 
            for boolean in default_columns_not_null
            if boolean
        ]
        columns_has_null = getColumnsNullPresence(self.anagrafica.df)

        # Test through all the columns
        for column_number, _ in enumerate(default_columns_must_be_not_null):
            # Conditional assertion test
            if columns_has_null[column_number] == True:
                column = self.anagrafica.df.iloc[:, column_number]
                rows_to_check = column.isna()
                for index, value in rows_to_check.iteritems():
                    # subTest allows no interruption if test fails
                    with self.subTest():
                        self.assertTrue(
                            value,
                            "Column {} has missing value ".format(column_number) + \
                            "in row {} :\n{}".format(
                                index, self.anagrafica.df.loc[index]
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
            column_series = self.anagrafica.df.iloc[:,column]
            # Test each row
            for index, value in column_series.iteritems():
                true_value = dateTextIsValid(value, self.anagrafica_date_format)
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