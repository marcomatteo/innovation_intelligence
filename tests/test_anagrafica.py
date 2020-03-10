import unittest as test
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO
import sys
sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")

from data_providers import AnagraficaInfocamere
from data_providers import (
    getColumnNames, getColumnsTypes, 
    getColumnsMaxLength, getColumnNullables,
    getBoolSeriesForDateChecking
)
from data_providers.dataProviderUtil import getTrimmedLength

from db_interface import I2FVG
from db_interface import getColumnsInfo, getNumpyTypesConversion

from log_test import LogCaptureRunner, BaseTestCase

LOG_FILE = "tests/logs/anag_infocamere.log"
logging.basicConfig(
    level = logging.DEBUG, # Only debug levels or higher
    format = "%(asctime)s %(levelname)-8s (%(funcName)s) %(message)s",
    datefmt = "%d-%m-%Y %H:%M:%S",
    filename = LOG_FILE,
    filemode = "w"
)

# Create logger
logger = logging.getLogger(__name__)

class Test_AnagraficaInfocamere(BaseTestCase):
    source_sheet_name = 'FRIULI anagrafica' # info non rilevante
    db_table_name = "TMP_IC_Anagrafica"
    
    columns_unique = [0, 1, 4]
    date_format = "%d/%m/%Y"
    
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        # create a in memory stream
        self.stream = StringIO()
        # add handler to logger
        self.handler = logging.StreamHandler(self.stream)
        logger.addHandler(self.handler)

    def tearDown(self, *args, **kwargs):
        super().tearDown(*args, **kwargs)
        # we're done with the caputre handler
        logger.removeHandler(self.handler) 

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None 
        logger.info("Apertura del file excel")
        cls.anagrafica = AnagraficaInfocamere("AnagraficaPreprocessed.xlsx")
        # cls.anagrafica = AnagraficaInfocamere("Infocamere_06feb2019bis.xlsx")
        # cls.anagrafica = AnagraficaInfocamere("Insiel.xlsx")
        logger.info("Aperto il file nella classe AnagraficaInfocamere")
        logger.info("Apertura connessione con il DB")
        cls.i2fvg = I2FVG()
        logger.info("Scarico le informazioni sulla tabella '%s'", cls.db_table_name)
        cls.db_info = cls.i2fvg.get_stats(cls.db_table_name)
        logger.info("Utilizzo funzione getColumnsInfo per riorganizzare le info dal DB")
        cls.db_columns_info = getColumnsInfo(cls.db_info, slice(0,-2))
        cls.default_columns_type = getNumpyTypesConversion(cls.db_columns_info.types)


    def test_acceptance_fileExtension_xls(self):
        test_fileExtension_type = self.anagrafica.file_ext
        self.assertEqual(
            test_fileExtension_type, 'xlsx',
            "Data Provider wrong extension. Expected xlsx extension!"
        )

    def test_acceptance_columnsNumber(self):
        default_columns_number = len(self.db_columns_info.names)
        logger.debug("Test numero di colonne presenti nel file: {}".format(
                        default_columns_number))
        test_columns_names_number = len(getColumnNames(self.anagrafica.df))
        self.assertEqual(
            test_columns_names_number, default_columns_number,
            "Data Provider wrong columns number"   
        )

    def test_acceptance_columnsTypes_int(self):
        default_cols_int = {i: col for i, col in self.default_columns_type.items() if 'int' in str(col)}
        logger.debug("Test sulle colonne di tipo 'int': ({})".format(", ".join(
            [str(key) + ": " + str(value)
                for key, value in default_cols_int.items()]
            ))
        )
        # seleziono le colonne tipo int
        selected_cols_df = self.anagrafica.df.iloc[:, list(default_cols_int.keys())]
        # casting
        try:
            col_casted = selected_cols_df.fillna(0).astype('int32')
        except:
            col_casted = selected_cols_df
        # Map with original column numbers
        test_columns_types = {
            i: ty 
            for i, ty in zip(
                default_cols_int.keys(), 
                getColumnsTypes(col_casted).values()
            )
        }
        self.assertEqual(
            test_columns_types, default_cols_int,
            "Selected columns [26, 28] must be np.dtype('int32')"
        )
    
    def test_acceptance_columnsTypes_float(self):
        default_cols_float = {i: col for i, col in self.default_columns_type.items() if 'float' in str(col)}
        logger.debug("Test sulle colonne di tipo 'float': ({})".format(", ".join(
            [str(key) + ": " + str(value)
                for key, value in default_cols_float.items()]
            ))
        )
        # seleziono le colonne tipo int
        selected_cols_df = self.anagrafica.df.iloc[:, list(default_cols_float.keys())]
        # casting
        try:
            col_casted = selected_cols_df.astype('float64')
        except:
            col_casted = selected_cols_df
        # Map with original column numbers
        test_columns_types = {
            i: ty 
            for i, ty in zip(
                default_cols_float.keys(), 
                getColumnsTypes(col_casted).values()
            )
        }
        self.assertEqual(
            test_columns_types, default_cols_float,
            "Selected columns [31] must be np.dtype('float64')"
        )
    
    def test_acceptance_columnsTypes_obj(self):
        default_cols_obj = {i: col for i, col in self.default_columns_type.items() if 'obj' in str(col)}
        logger.debug("Test sulle colonne di tipo 'object': ({})".format(", ".join(
            [str(key) + ": " + str(value)
                for key, value in default_cols_obj.items()]
            ))
        )
        # seleziono le colonne tipo int
        selected_cols_df = self.anagrafica.df.iloc[:, list(default_cols_obj.keys())]
        # casting
        try:
            col_casted = selected_cols_df.astype('object')
        except:
            col_casted = selected_cols_df
        # Map with original column numbers
        test_columns_types = {
            i: ty 
            for i, ty in zip(
                default_cols_obj.keys(), 
                getColumnsTypes(col_casted).values()
            )
        }
        self.assertEqual(
            test_columns_types, default_cols_obj,
            "Selected columns must be np.dtype('object')"
        )

    def test_acceptance_columnsMaxLength(self):
        default_cols_max_lenght = self.db_columns_info.lengths
        logger.debug("Test sulla lunghezza massima delle colonne: ({})".format(", ".join(
            [str(key) + ": " + str(value)
                for key, value in enumerate(default_cols_max_lenght)]
            ))
        )
        
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
                            self.assertGreaterEqual(
                                value_lenght, max_lenght, 
                                "Column {}, row {} has {}".format(
                                    column_number, index, value_lenght
                                )
                            )
    
    def test_acceptance_columnsNullable(self):
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
                    self.assertListEqual(
                        missing_list, [], # Empty list
                        "Trovati valori mancanti!\n" + \
                        "Colonna n. {}\n".format(column_number) + \
                        "Indici: {}".format(missing_list) 
                    )
        
        logger.debug("Test sulle colonne nullable: ({})".format(", ".join(
            [str(key) + ": " + str(value)
                for key, value in enumerate(default_cols_nullables)]
            ))
        )
        
    def test_acceptance_columnsDateFormat(self):
        # Seleziono le colonne che da DB devono risultare come date
        default_cols_date = {i: col for i, col in self.default_columns_type.items() if 'date' in str(col)}

        selected_cols_df = self.anagrafica.df.iloc[:, list(default_cols_date.keys())]
        result_series = selected_cols_df.agg(
                lambda x: getBoolSeriesForDateChecking(x, self.date_format),
                axis = 0
            )
        result_toLog = result_series.tolist()
        # Stampo le colonne da DB su file di log
        logger.debug("Test sulle colonne data: ({})".format(", ".join(
            [str(key) + ": " + str(value)
                for key, value in zip(default_cols_date.keys(), result_toLog)]
            ))
        )
        self.assertTrue(
            result_series.all(),
            "The dataframe has columns with incorrect date format"
        )
        
if __name__ == '__main__':
    loader = test.TestLoader()
    suite = loader.loadTestsFromTestCase(Test_AnagraficaInfocamere)
    runner = LogCaptureRunner(verbosity=2)
    runner.run(suite)