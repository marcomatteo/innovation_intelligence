import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)
    
import unittest as test
from idb import DatabaseConnector

class Test_DatabaseConnector(test.TestCase):

    def setUp(self):
        self.ii = DatabaseConnector()

    def test_mod_Test(self):
        self.ii.inTest = True
        self.assertEqual("Test", self.ii.mod)

    def test_mod_Data(self):
        self.ii.inTest = False
        self.assertEqual("Data", self.ii.mod)

    def test_connessione_test(self):
        self.ii.inTest = True
        self.assertEqual(
            "mssql+pyodbc://I2FVGTestReader:I2FVGTestReader@I2FVG_TEST", 
            self.ii.connection_string)

    def test_connessione_data(self):
        self.ii.inTest = False
        self.assertEqual(
            "mssql+pyodbc://I2FVGDataReader:I2FVGDataReader@I2FVG_DATA_dev", 
            self.ii.connection_string)

    def tearDown(self):
        del self.ii