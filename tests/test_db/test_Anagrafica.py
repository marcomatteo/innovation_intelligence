import unittest
# from unittest.mock import ...
from idb import Anagrafica

class Test_Anagrafica(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.anagrafica = Anagrafica()

    def setUp(self):
        self.anagrafica.inTest = True

    def test_mod_Test(self):
        self.assertEqual("Test", self.anagrafica.mod)

    def test_mod_Data(self):
        self.anagrafica.inTest = False
        self.assertEqual("Data", self.anagrafica.mod)

    def test_connessione_test(self):
        self.assertEqual(
            "mssql+pyodbc://I2FVGTestReader:I2FVGTestReader@I2FVG_TEST", 
            self.anagrafica.connection_string)

    def test_connessione_data(self):
        self.anagrafica.inTest = False
        self.assertEqual(
            "mssql+pyodbc://I2FVGDataReader:I2FVGDataReader@I2FVG_DATA_dev", 
            self.anagrafica.connection_string)

    def test_get_fiscalcode_list(self):
        cf_list = [
            '00001510288'
            , '00002070324'
            , '00004280327'
            , '00007080369'
            , '00007470933'
        ]
        self.assertEqual(
            cf_list,
            self.anagrafica.get_fiscalcode_list()[:5])

    def test_get_sedi_imprese_return_DataFrame(self):
        import pandas as pd        

        self.assertEqual(
            pd.DataFrame,
            type(self.anagrafica.get_sedi_imprese())
        )