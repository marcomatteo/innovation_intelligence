import sys
from tests import TestAcceptanceBaseClass
from utilities import create_logger
from acceptance_builder import AnagraficaBuilder

class Test_AnagraficaInfocamereAcceptance(TestAcceptanceBaseClass):
    LOG_DIR = None

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.logger = create_logger("AnagraficaInfocamere", cls.LOG_DIR)
        cls.cert = AnagraficaBuilder()
        super().setUpClass()

    def test_acceptance_column_innovativa(self):
        """
        Controllo valori possibili: [NO, SI]
        """
        self.logger.debug("Check colonna PMI Innovativa")

        n_col = 42
        test_values = ['NO', 'SI']
        dp_values = self.cert.dp.df.iloc[:, n_col] \
            .value_counts().sort_index().index.tolist()
        self.logger.debug("Valori da controllare: ({})"
                     .format(", ".join(dp_values)))

        try:
            self.assertEqual(
                dp_values,
                test_values,
                "Valori non ammessi per la colonna {}!".format(n_col)
            )
        except Exception as e:
            self.logger.exception(e)
            raise e
        
        self.logger.debug("Test OK\n\n")

    def test_acceptance_column_femminile(self):
        """
        Controllo valori possibili: ['NO', 'Esclusiva', 'Forte', 'Maggioritaria']
        """
        self.logger.debug("Check colonna Impresa Femminile")

        n_col = 44
        test_values = ['Esclusiva', 'Forte', 'Maggioritaria', 'NO']

        dp_values = self.cert.dp.df.iloc[:, n_col] \
            .value_counts().sort_index().index.tolist()
        self.logger.debug("Valori da controllare: ({})"
                     .format(", ".join(dp_values)))

        try:
            self.assertEqual(
                dp_values,
                test_values,
                "Valori non ammessi per la colonna {}!".format(n_col)
            )
        except Exception as e:
            self.logger.exception(e)
            raise e

        self.logger.debug("Test OK\n\n")

    def test_acceptance_column_giovanile(self):
        """
        Controllo valori possibili: ['NO', 'Esclusiva', 'Forte', 'Maggioritaria']
        """
        self.logger.debug("Check colonna Impresa Giovanile")

        n_col = 45
        test_values = ['Esclusiva', 'Forte', 'Maggioritaria', 'NO']

        dp_values = self.cert.dp.df.iloc[:, n_col] \
            .value_counts().sort_index().index.tolist()
        self.logger.debug("Valori da controllare: ({})"
                     .format(", ".join(dp_values)))

        try:
            self.assertEqual(
                dp_values,
                test_values,
                "Valori non ammessi per la colonna {}!".format(n_col)
            )
        except Exception as e:
            self.logger.exception(e)
            raise e

        self.logger.debug("Test OK\n\n")

    def test_acceptance_column_straniera(self):
        """
        Controllo valori possibili: ['NO', 'Esclusiva', 'Forte', 'Maggioritaria']
        """
        self.logger.debug("Check colonna Impresa Straniera")

        n_col = 46
        test_values = ['Esclusiva', 'Forte', 'Maggioritaria', 'NO']
        
        dp_values = self.cert.dp.df.iloc[:, n_col] \
            .value_counts().sort_index().index.tolist()
        
        self.logger.debug("Valori da controllare: ({})"
                     .format(", ".join(dp_values)))
        
        try:
            self.assertEqual(
                dp_values,
                test_values,
                "Valori non ammessi per la colonna {}!".format(n_col)
            )
        except Exception as e:
            self.logger.exception(e)
            raise e

        self.logger.debug("Test OK\n\n")


if __name__ == "__main__":
    from unittest import main

    if len(sys.argv) > 1:
        Test_AnagraficaInfocamereAcceptance.LOG_DIR = sys.argv.pop()

    main(verbosity=2)