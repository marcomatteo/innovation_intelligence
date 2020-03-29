import unittest as test
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO
from collections import defaultdict
import sys
sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")

from data_providers import Accredia
from data_providers import (
    getColumnNames, getColumnsTypes, 
    getColumnsMaxLength, getColumnNullables,
    getColumnTest, getTableTest,
    isValidDateFormat, getTrimmedLength
)

from db_interface import I2FVG
from db_interface import getColumnsInfo, getNumpyTypesConversion

from log_test import LogCaptureRunner, BaseTestCase

LOG_FILE = "tests/logs/Accredia/{}.md".format(datetime.today().strftime('%Y-%m-%d'))
logging.basicConfig(
    level = logging.DEBUG, # Only debug levels or higher
    format = "%(asctime)s %(levelname)-8s (%(funcName)s) %(message)s",
    datefmt = "%d-%m-%Y %H:%M:%S",
    filename = LOG_FILE,
    filemode = "w"
)

class Test_Accredia(BaseTestCase):
    file_name = "20200203_accredia.csv" 
    db_table_name = "TMP_AC_Certificazioni"
    columns_unique = [0, 4]
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None

        # Create logger
        cls.logger = logging.getLogger(__name__)    
        super().logInfoTitle("Test Data Provider : Accredia")

        super().logInfoMessage("Apertura del file excel...")
        try:
            cls.anagrafica = Accredia(cls.file_name)
        except:
            super().logErrorMessage("Errore apertura file '{}'!".format(cls.file_name))
        
        super().logInfoMessage("Apertura connessione con il DB...")
        try:
            cls.i2fvg = I2FVG()
        except:
            super().logErrorMessage("Errore connessione con il DB!")
        
        super().logInfoMessage("Scarico le informazioni sulla tabella '{}'...".format(
            cls.db_table_name
        ))
        try:
            cls.db_info = cls.i2fvg.get_stats(cls.db_table_name)
        except:
            super().logErrorMessage("Impossibile scaricare le informazioni dalla tabella {}".format(
                cls.db_table_name))

        # Formatto info dal DB per i controlli    
        cls.db_columns_info = getColumnsInfo(cls.db_info, slice(1,-2))
        cls.default_columns_type = getNumpyTypesConversion(cls.db_columns_info.types)

        # Log info del data provider
        super().logDataFrameInfo(cls.anagrafica.df)
        cls.logger.info("\n\n{}".format(super().log_new_line))

    def test_acceptance_fileExtension_xls(self):
        test_fileExtension_type = self.anagrafica.file_ext
        extension = "csv"
        # Log to file
        self.logger.debug("\n\n### Test Acceptance Estensione\n")
        self.logDifferences([extension], [self.anagrafica.file_ext])

        self.assertEqual(
            test_fileExtension_type, extension,
            "Data Provider wrong extension. Expected xlsx extension!"
        )

    def test_acceptance_columnsNumber(self):
        # Log to file
        self.logTestTile("Test Acceptance Columns Number")

        default_columns_number = len(self.db_columns_info.names)
        data_provider_names = getColumnNames(self.anagrafica.df)
        
        # Log diffs
        self.logDifferences(self.db_columns_info.names, data_provider_names)

        test_columns_names_number = len(data_provider_names)
        self.assertEqual(
            test_columns_names_number, default_columns_number,
            "Data Provider wrong columns number"   
        )

    def test_acceptance_columnsTypes_int(self):
        # Log to file
        self.logTestTile("Test Acceptance Columns Int Type")
        # Seleziono le colonne dalle info del DB
        default_cols_int = {
                i: col 
                for i, col in self.default_columns_type.items()
                if 'int' in str(col)
            }
        test_columns_types = dict()
        cast_result = dict()
        # seleziono le colonne tipo int
        for num_col in default_cols_int.keys():
            selected_cols_df = self.anagrafica.df.iloc[:, num_col].to_frame()
            # casting
            try:
                col_casted = selected_cols_df.fillna(0).astype('int32')
                cast_result[num_col] = True
            except:
                cast_result[num_col] = False
                col_casted = selected_cols_df
            test_columns_types[num_col] = getColumnsTypes(col_casted).popitem()[1]

        # LOG
        self.logDifferences_types(self.anagrafica.df, cast_result)

        self.assertEqual(
            test_columns_types, default_cols_int,
            "Selected columns [26, 28] must be np.dtype('int32')"
        )
    
    def test_acceptance_columnsTypes_float(self):
        # Log to file
        self.logTestTile("Test Acceptance Columns Float Type")
        # Seleziono le colonne dalle info del DB
        default_cols_float = {
                i: col 
                for i, col in self.default_columns_type.items() 
                if 'float' in str(col)
            }
        # seleziono le colonne tipo float
        selected_cols_df = self.anagrafica.df.iloc[:, list(default_cols_float.keys())]
        test_columns_types = dict()
        cast_result = dict()
        for num_col in default_cols_float.keys():
            selected_cols_df = self.anagrafica.df.iloc[:, num_col].to_frame()
            # casting
            try:
                col_casted = selected_cols_df.astype('float64')
                cast_result[num_col] = True
            except:
                cast_result[num_col] = False
                col_casted = selected_cols_df
            test_columns_types[num_col] = getColumnsTypes(col_casted).popitem()[1]
        # LOG
        self.logDifferences_types(self.anagrafica.df, cast_result)
        self.assertEqual(
            test_columns_types, default_cols_float,
            "Selected columns [31] must be np.dtype('float64')"
        )
    
    def test_acceptance_columnsTypes_obj(self):
        # Log to file
        self.logTestTile("Test Acceptance Columns Object Type")
        # Seleziono le colonne dalle info del DB
        default_cols_obj = {
                i: col 
                for i, col in self.default_columns_type.items() 
                if 'obj' in str(col)
            }
        # seleziono le colonne tipo object
        selected_cols_df = self.anagrafica.df.iloc[:, list(default_cols_obj.keys())]
        test_columns_types = dict()
        cast_result = dict()
        for num_col in default_cols_obj.keys():
            selected_cols_df = self.anagrafica.df.iloc[:, num_col].to_frame()
            # casting
            try:
                col_casted = selected_cols_df.astype('object')
                cast_result[num_col] = True
            except:
                cast_result[num_col] = False
                col_casted = selected_cols_df
            test_columns_types[num_col] = getColumnsTypes(col_casted).popitem()[1]
        # LOG
        self.logDifferences_types(self.anagrafica.df, cast_result)
        self.assertEqual(
            test_columns_types, default_cols_obj,
            "Selected columns must be np.dtype('object')"
        )

    def test_acceptance_columnsMaxLength(self):
        # Log to file
        self.logTestTile("Test Acceptance Columns Max Lenght")
        default_cols_max_lenght = self.db_columns_info.lengths
        test_columns_max_lenght = getColumnsMaxLength(self.anagrafica.df)

        # Test through all the columns
        for column_number, max_lenght in enumerate(default_cols_max_lenght):
            # If not Null
            if max_lenght:
                # Conditional assertion test
                if test_columns_max_lenght[column_number] > max_lenght:
                    column = self.anagrafica.df.iloc[:, column_number].map(
                        lambda x: getTrimmedLength(x))
                    condition = column > max_lenght
                    rows_to_check = column.loc[condition]
                    #TODO: sostituire iteritems() con metodo vettorizzato
                    for index, value in rows_to_check.iteritems():
                        # subTest allows no interruption if test fails
                        with self.subTest(max = max_lenght):
                            value_lenght = len(str(value).strip())
                            try:
                                self.assertGreaterEqual(
                                    value_lenght, max_lenght, 
                                    "Column {}, row {} has {}".format(
                                        column_number, index, value_lenght
                                    )
                                )
                            except AssertionError:
                                pass

        self.logDifferences(default_cols_max_lenght, test_columns_max_lenght)

    def test_acceptance_columnsNullable(self):
        column_inspector = defaultdict(list)
        # Log to file
        self.logTestTile("Test Acceptance Columns Nullables")
        default_cols_nullables = self.db_columns_info.nullables
        test_columns_nullables = getColumnNullables(self.anagrafica.df)

        # Iterazione di tutte le colonne
        for column_number, _ in enumerate(default_cols_nullables):
            # Effettuo il controllo solo se False -> non può essere nullable (null)
            if test_columns_nullables[column_number] == False:
                # Seleziono la colonna
                column = self.anagrafica.df.iloc[:, column_number]
                # Boolean vector per selezionare i campi NA (null)
                col_to_check = column.isna()
                # Lista delle posizioni nel vettore in cui mancano i valori
                missing_list = self.anagrafica.df.loc[col_to_check].index.values.tolist()
                with self.subTest():
                    try:
                        self.assertListEqual(
                            missing_list, [], # Empty list
                            "Trovati valori mancanti!\n" + \
                            "Colonna n. {}\n".format(column_number) + \
                            "Indici: \n{}".format(", ".join(missing_list)) 
                        )
                    except AssertionError:
                        column_inspector[column_number] = missing_list
        
        self.logObject(column_inspector)
        self.logDifferences(default_cols_nullables, test_columns_nullables)
        
    def test_validity_keys(self):
        # Log to file
        self.logTestTile("Test Validity Primary Keys")
        pk_columns = self.anagrafica.df.iloc[:, self.columns_unique].columns.tolist()
        test_duplicated = self.anagrafica.df.duplicated(
            subset = pk_columns
        )
        if test_duplicated.sum() > 0:
            self.logger.debug("\n\n**Test no ok**\n")
            self.logDataFrame(
                self.anagrafica.df.loc[test_duplicated],
                pk_columns
            )
        else:
            self.logger.debug("\n\n**Test ok**\n")
            cols = [", ".join(pk_columns)]
            self.logDifferences(
                cols, 
                {0:False}
            )


if __name__ == '__main__':
    loader = test.TestLoader()
    suite = loader.loadTestsFromTestCase(Test_Accredia)
    runner = LogCaptureRunner(verbosity=2)
    runner.run(suite)