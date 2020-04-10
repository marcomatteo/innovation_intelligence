import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)
    
import unittest as test
from idb import II2FVG

class Test_II2FVG(test.TestCase):

    def setUp(self):
        self.ii = II2FVG()

    def test_mod_Test(self):
        self.ii.test = True
        self.assertEqual("Test", self.ii.mod)

    def test_mod_Data(self):
        self.ii.test = False
        self.assertEqual("Data", self.ii.mod)

    def test_connessione_test(self):
        self.ii.test = True
        self.assertEqual(
            "mssql+pyodbc://I2FVGTestReader:I2FVGTestReader@I2FVG_TEST", 
            self.ii.connessione)

    def test_connessione_data(self):
        self.ii.test = False
        self.assertEqual(
            "mssql+pyodbc://I2FVGDataReader:I2FVGDataReader@I2FVG_DATA_dev", 
            self.ii.connessione)

    def tearDown(self):
        del self.ii