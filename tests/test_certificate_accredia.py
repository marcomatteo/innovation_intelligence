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

    def test_MatchAllRowsFromDataProvider_EmptyDataFrame(self):
        
        def trim_cols(col):
            return col.map(lambda x: str(x).strip())

        self.logTestTile("Test su ogni certificazione importata")

        custom_dp_df = self.data_dp.drop(columns='id_istat_province').apply(
            lambda x: trim_cols(x))
        custom_db_df = self.data_db.iloc[:, [1, 2, 3, 9]].apply(
            lambda x: trim_cols(x))

        # CF, PV e CodiceCertificazione sono univoci
        custom_dp_df.set_index(
            ['CF', "PV", "CodiceCertificazione"], inplace = True)
        custom_db_df.set_index(
            ["CF", "ID_Provincia", "CodiceCertificazione"], inplace = True
        )

        # Rename indici per il join
        names = ["CF", "PV", "Cert"]
        custom_dp_df.index.set_names(names, inplace = True)
        custom_db_df.index.set_names(names, inplace = True)

        df_join = custom_dp_df.join(
            custom_db_df,
            how = "left"
        )

        # Verifico che non ci siano record non importati
        cond = df_join['DataCertificazione'].isna()
        df_cond = cond.reset_index()
        df_check = df_cond.loc[df_cond['DataCertificazione'] == True]
        assertion = df_check.empty

        # LOG if there is some missing
        if ~ assertion:
            df_check.index.set_names("Indice", inplace=True)
            message = "Nella tabella ci sono certificazioni non importate.\n" + \
                "Nella colonna DataCertificazione e' indicato con ```True``` che la " + \
                "certificazione e' mancante."
            self.logDataFrame(df=df_check, message=message)

        self.assertTrue(
            assertion,
            "Ci sono {} certificazioni non importate".format(
                df_check.shape[0])
        )


if __name__ == '__main__':
    loader = test.TestLoader()
    suite = loader.loadTestsFromTestCase(Test_CertificazioneAccredia)
    runner = LogCaptureRunner(verbosity=2)
    runner.run(suite)
