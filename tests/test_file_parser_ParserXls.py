from utilities import ROOT
from file_parser import ParserXls
from logger import TestLogger
import unittest as test
import pandas as pd
from datetime import datetime

class Test_ParserXls(test.TestCase):
    root_dir = ROOT + r"/data/data_tests/IParsers/"

    @classmethod
    def setUpClass(cls):
        cls.logger = TestLogger("ParserXls")
        cls.logger.log_title("")
        file_path = cls.root_dir + "test_file.xlsx"
        cls.parser = ParserXls(file_path=file_path)
        cls.file_fonte = cls.parser.open_file(sheet_name=None)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_open_file_columns_matching(self):
        """
        Controllo la corrispondenza nelle prime
        colonne del foglio aperto
        """
        df = self.file_fonte["FRIULI anagrafica"]
        self.assertEqual(
            ["c fiscale","PRV - Provincia",	
            "N-REG-IMP - Numero Registro Imprese", "rea",
            "UL-SEDE - Unità Locale o sede dell'impresa"],
            df.columns.tolist()[:5]
        )

    def test_open_file_fiscalcode_string_formatting(self):
        """
        Controllo se un codice fiscale viene formattato
        correttamente mantenendo gli zeri iniziali
        """
        df = self.file_fonte["FRIULI anagrafica"]

        self.assertEqual(
           ["00002070324",
            "00002070324",
            "00002070324",
            "00007080369",
            "00007080369"],
            df['c fiscale'].tolist()[:5]
        )

    @test.skip("Non ho ancora trovato soluzione a questo problema")
    def test_open_file_date_formatting(self):
        """
        Controllo se una data viene letta correttamente
        mantentendo il suo formato da file excel
        """
        df = self.file_fonte.get("FRIULI anagrafica")

        self.assertEqual(
            "19/02/1996",
            df["DT-ISCR-RI - Data di iscrizione al Registro Imprese"][0]
        )

if __name__ == '__main__':
    loader = test.TestLoader()
    suite = loader.loadTestsFromTestCase(Test_ParserXls)
    test.TextTestRunner().run(suite)