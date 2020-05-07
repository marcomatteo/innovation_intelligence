import unittest
from unittest.mock import patch
from idb import DatabaseConnector

class Test_DatabaseConnector(unittest.TestCase):

    def setUp(self):
        self.ii = DatabaseConnector()

    def test_mod_Test(self):
        self.assertEqual("Test", self.ii.mod)

    def test_mod_Data(self):
        self.ii.inTest = False
        self.assertEqual("Data", self.ii.mod)

    def test_connessione_test(self):
        self.assertEqual(
            "mssql+pyodbc://I2FVGTestReader:I2FVGTestReader@I2FVG_TEST", 
            self.ii.connection_string)

    def test_connessione_data(self):
        self.ii.inTest = False
        self.assertEqual(
            "mssql+pyodbc://I2FVGDataReader:I2FVGDataReader@I2FVG_DATA_dev", 
            self.ii.connection_string)

    def test_tables_number(self):
        tables = self.ii.tables
        self.assertEqual(65, len(tables))

    def test_open_table_return_DataFrame(self):
        import pandas as pd        
        table_name = "SYSTEM_DataProviderInfo"
        self.assertEqual(
            pd.DataFrame,
            type(self.ii.open_table(table_name))
        )

    def test_open_table_exception_raised(self):
        table_name = "TABLE_TEST"
        with self.assertRaises(KeyError) as cm:
            df = self.ii.open_table(table_name)

        the_exception = cm.exception
        self.assertEqual(
            str(the_exception),
            "'Invalid table name! No TABLE_TEST in DB!'")

    def tearDown(self):
        del self.ii