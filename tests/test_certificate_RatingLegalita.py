import logging
import unittest as test
import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO

from data_provider import RatingLegalita
from db_interface import I2FVG
from certificates import trim_columns_spaces, dataframe_index_differences
from log_test import LogCaptureRunner, BaseTestCase

LOG_FILE = r"logs/markdowns/cert_import_RatingLegalita.md"
logging.basicConfig(
    level = logging.DEBUG, # Only debug levels or higher
    format = "%(asctime)s %(levelname)-8s (%(funcName)s) %(message)s",
    datefmt = "%d-%m-%Y %H:%M:%S",
    filename = LOG_FILE,
    filemode = "w"
)

class Test_CertificazioneRatingLegalita(BaseTestCase):
    # Data Provider file name
    dp_keys = ['Codice fiscale', 'Rating']
    db_keys = ['CF', 'Rating']
    # Ricostruisco i dati nel DB come sono nel file fonte
    db_query = "SELECT Procedimento, CF, DataEsito, Esito"\
                + ", Rating, ScadenzaRevocaSospensione " \
                + "FROM DATA_RatingLegalita"

    @classmethod
    def setUpClass(cls):
        anno = datetime.now().year
        # Create logger
        cls.logger = logging.getLogger(__name__)    
        super().logInfoTitle(
            "Test Certificazione Data Provider : Rating Legalita {}".format(anno))

        super().logInfoMessage("Carico le tabelle sul DB...")
        cls.ii = I2FVG()
        
        cf_list = cls.ii.get_fiscalcode_list()
        cls.data_db = pd.read_sql_query(cls.db_query, cls.ii.engine)
        cls.data_db = cls.data_db.apply(lambda col: trim_columns_spaces(col))
        cls.data_db.set_index(cls.db_keys, inplace = True)
        
        super().logInfoMessage("Carico file data provider...")
        try:
            cls.dp = RatingLegalita()
        except:
            super().logErrorMessage("Errore apertura file '{}'!".format(cls.dp.file_path))
        
        cls.dp.update_rating_column_with_spaces()
        cls.data_dp = cls.dp.get_filtred_fiscal_codes_dataframe(cf_list)
        cls.data_dp = cls.data_dp.apply(lambda col: trim_columns_spaces(col))
        cls.data_dp.set_index(cls.dp_keys, inplace = True)
        
        super().logNewLine()

    def test_index_comparison_with_utility_function(self):
        
        self.logTestTile("Test su ogni anagrafica importata")

        dp = self.data_dp.copy()
        db = self.data_db.copy()

        # Creo una colonna fittizia per il confronto
        db['col1'] = "presente"

        names = self.db_keys
        dp.index.set_names(names, inplace = True)
        db.index.set_names(names, inplace = True)
        df_check = dataframe_index_differences( dp, db, how='left')

        # LOG if there is some missing
        if ~ df_check.empty:
            df_check.reset_index().index.set_names("Indice", inplace=True)
            message = f"Nella tabella ci sono {df_check.shape[0]} righe non importate.\n"
            self.logDataFrame(df=df_check, message=message)

        self.assertTrue(
            df_check.empty,
            f"Inner join left tra i due df ha {df_check.shape[0]} valori mancanti"
        )



if __name__ == '__main__':
    loader = test.TestLoader()
    suite = loader.loadTestsFromTestCase(Test_CertificazioneRatingLegalita)
    runner = LogCaptureRunner(verbosity=2)
    runner.run(suite)
