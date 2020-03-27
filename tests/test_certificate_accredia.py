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
        super().logInfoMessage("Carico le tabelle sul DB")
        cls.db = Certificazione()
        cls.data_db = cls.db.df

    def test_NuoviCodiceCertificazioni_vuoto(self):
        self.logTestTile("Test nuovi CodiceCertificazioni")

        dp_set = set(self.dp.get_certificazioni())
        db_set = set(self.db.get_certificazioni())

        # Controllo che le tipologie del dp siano importate tutte
        differences = set.difference(dp_set, db_set)
        self.logObject(differences)
        self.assertTrue(
            len(differences) == 0,
            "Sono presenti tipologie di Certificazioni non importate"
        )

    def test_MatchRowsWithNamedTuples(self):
        
        def trim_cols(col):
            return col.map(lambda x: str(x).strip())

        def load_dataProvider_list(df) -> list:
            match_list = list()
            for row in df.itertuples(name="Certificazioni", index=False):
                match_list.append(row)
            return match_list

        # self.logTestTile("Test su ogni certificazione importata")

        custom_dp_df = self.data_dp.drop(columns='id_istat_province').apply(lambda x: trim_cols(x))
        custom_db_df = self.data_db.iloc[:, [1, 2, 3, 9]]

        dp_list = load_dataProvider_list(custom_dp_df)
        db_list = load_dataProvider_list(custom_db_df)

        dp_set = set(dp_list)
        db_set = set(db_list)

        differences = set.difference(dp_set, db_set)
        self.logObject(differences)

        self.assertTrue(
            len(differences) == 0,
            "Alcune certificazioni non corrispondono"
        )

if __name__ == '__main__':
    loader = test.TestLoader()
    suite = loader.loadTestsFromTestCase(Test_CertificazioneAccredia)
    runner = LogCaptureRunner(verbosity=2)
    runner.run(suite)
