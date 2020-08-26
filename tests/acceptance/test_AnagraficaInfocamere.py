from tests import TestAcceptanceBaseClass
from acceptance_builder import AnagraficaBuilder

import unittest
import numpy as np
import logging
from datetime import datetime

LOG_FILE = datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-5s %(name)-8s (%(funcName)s) %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    filename=r"logs/acceptance_tests/AnagraficaInfocamere/" + LOG_FILE,
    filemode="w"
)
logger = logging.getLogger(__name__)


class Test_AnagraficaInfocamereAcceptance(TestAcceptanceBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        logger.debug("Inizio Test_AnagraficaInfocamereAcceptance... ")
        cls.cert = AnagraficaBuilder()

    def test_acceptance_column_innovativa(self):
        """
        Controllo valori possibili: [NO, SI]
        """
        logger.debug("Check colonna PMI Innovativa")

        n_col = 42
        test_values = ['NO', 'SI']
        dp_values = self.cert.dp.df.iloc[:, n_col] \
            .value_counts().sort_index().index.tolist()
        logger.debug("Valori da controllare: ({})"
                     .format(", ".join(dp_values)))

        try:
            self.assertEqual(
                dp_values,
                test_values,
                "Valori non ammessi per la colonna {}!".format(n_col)
            )
        except Exception as e:
            logger.exception(e)
            raise e
        
        logger.debug("Test OK")

    def test_acceptance_column_femminile(self):
        """
        Controllo valori possibili: ['NO', 'Esclusiva', 'Forte', 'Maggioritaria']
        """
        logger.debug("Check colonna Impresa Femminile")

        n_col = 44
        test_values = ['Esclusiva', 'Forte', 'Maggioritaria', 'NO']

        dp_values = self.cert.dp.df.iloc[:, n_col] \
            .value_counts().sort_index().index.tolist()
        logger.debug("Valori da controllare: ({})"
                     .format(", ".join(dp_values)))

        try:
            self.assertEqual(
                dp_values,
                test_values,
                "Valori non ammessi per la colonna {}!".format(n_col)
            )
        except Exception as e:
            logger.exception(e)
            raise e

        logger.debug("Test OK")

    def test_acceptance_column_giovanile(self):
        """
        Controllo valori possibili: ['NO', 'Esclusiva', 'Forte', 'Maggioritaria']
        """
        logger.debug("Check colonna Impresa Giovanile")

        n_col = 45
        test_values = ['Esclusiva', 'Forte', 'Maggioritaria', 'NO']

        dp_values = self.cert.dp.df.iloc[:, n_col] \
            .value_counts().sort_index().index.tolist()
        logger.debug("Valori da controllare: ({})"
                     .format(", ".join(dp_values)))

        try:
            self.assertEqual(
                dp_values,
                test_values,
                "Valori non ammessi per la colonna {}!".format(n_col)
            )
        except Exception as e:
            logger.exception(e)
            raise e

        logger.debug("Test OK")


    def test_acceptance_column_straniera(self):
        """
        Controllo valori possibili: ['NO', 'Esclusiva', 'Forte', 'Maggioritaria']
        """
        logger.debug("Check colonna Impresa Straniera")

        n_col = 46
        test_values = ['Esclusiva', 'Forte', 'Maggioritaria', 'NO']
        
        dp_values = self.cert.dp.df.iloc[:, n_col] \
            .value_counts().sort_index().index.tolist()
        
        logger.debug("Valori da controllare: ({})"
                     .format(", ".join(dp_values)))
        
        try:
            self.assertEqual(
                dp_values,
                test_values,
                "Valori non ammessi per la colonna {}!".format(n_col)
            )
        except Exception as e:
            logger.exception(e)
            raise e

        logger.debug("Test OK")


if __name__ == "__main__":
    from unittest import main
    main(verbosity=2)