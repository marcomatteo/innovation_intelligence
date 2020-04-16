import sys
import logging
import unittest as test
import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO

sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")

from data_providers import Accredia
from db_interface import I2FVG, Certificazione
from certificates import trim_columns_spaces, dataframe_index_differences
from log_test import LogCaptureRunner, BaseTestCase

LOG_FILE = "tests/logs/certificazioni/accredia.md"
logging.basicConfig(
    level = logging.DEBUG, # Only debug levels or higher
    format = "%(asctime)s %(levelname)-8s (%(funcName)s) %(message)s",
    datefmt = "%d-%m-%Y %H:%M:%S",
    filename = LOG_FILE,
    filemode = "w"
)

class Test_CertificazioneAccredia(BaseTestCase):
    # Data Provider file name
    dp_file_name = "20200203_accredia.csv"

    @classmethod
    def setUpClass(cls):
        anno = datetime.now().year
        # Create logger
        cls.logger = logging.getLogger(__name__)    
        super().logInfoTitle(
            "Test Certificazione Data Provider : Accredia {}".format(anno))

        super().logInfoMessage("Creo connessione con il db e ottengo lista cf...")
        
        cls.ii = I2FVG(True)
        cf_list = cls.ii.get_fiscalcode_list()
        
        super().logInfoMessage("Carico file data provider...")
        cls.dp = Accredia(cls.dp_file_name)
        cls.dp.set_selected_fiscalcodes(cf_list)
        cls.dp.set_renamed_df()
        cls.data_dp = cls.dp.df
        cls.data_dp = cls.data_dp.apply(lambda col: trim_columns_spaces(col))
        cls.data_dp.drop(columns='id_istat_province', inplace=True)
        
        super().logInfoMessage("Carico le tabelle sul DB")
        cls.db = Certificazione()
        cls.data_db = cls.db.df
        cls.data_db = cls.data_db.apply(lambda col: trim_columns_spaces(col))
        super().logNewLine()

    def test_NewCodiceCertificazioni_ZeroDifferences(self): 
        self.logTestTile("Test nuovi CodiceCertificazioni")

        dp_set = set(self.dp.get_certificazioni())
        db_set = set(self.db.get_certificazioni())

        # Controllo che le tipologie del dp siano importate tutte
        differences = set.difference(dp_set, db_set)
        assertion = len(differences) == 0
        if ~ assertion:
            self.logSeries([diff for diff in differences])
        
        self.assertTrue(
            assertion,
            "Sono presenti n. {} tipologie di Certificazioni non importate".format(
                len(differences)
            )
        )

    def test_index_comparison_with_utility_function(self):
        
        self.logTestTile("Test su ogni certificazione importata con funzione Utility")

        custom_dp_df = self.data_dp.copy()
        custom_db_df = self.data_db.iloc[:, [1, 2, 3, 9]].copy()

        # CF, PV e CodiceCertificazione sono univoci
        custom_dp_df.set_index(
            ['CF', "PV", "CodiceCertificazione"], inplace = True)
        custom_db_df.set_index(
            ["CF", "ID_Provincia", "CodiceCertificazione"], inplace = True
        )

        df_check = dataframe_index_differences(
            custom_dp_df,
            custom_db_df,
            how='left'
        )

        # LOG if there is some missing
        if ~ df_check.empty:
            df_check.reset_index().index.set_names("Indice", inplace=True)
            message = f"Nella tabella ci sono {df_check.shape[0]} certificazioni non importate.\n" + \
                "Nella colonna DataCertificazione e' indicato con ```True``` che la " + \
                "certificazione e' mancante."
            self.logDataFrame(df=df_check, message=message)

        self.assertTrue(
            df_check.empty,
            f"Inner join left tra i due df ha {df_check.shape[0]} valori mancanti"
        )



if __name__ == '__main__':
    loader = test.TestLoader()
    suite = loader.loadTestsFromTestCase(Test_CertificazioneAccredia)
    runner = LogCaptureRunner(verbosity=2)
    runner.run(suite)
