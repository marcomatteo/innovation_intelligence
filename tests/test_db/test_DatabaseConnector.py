import unittest
from unittest import main
from unittest.mock import patch
from idb import DatabaseConnector


class Test_DatabaseConnector(unittest.TestCase):

    maxDiff = None

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
            type(self.ii.get_dataframe_from_table(table_name))
        )

    def test_open_table_exception_raised(self):
        table_name = "TABLE_TEST"
        with self.assertRaises(KeyError) as cm:
            df = self.ii.get_dataframe_from_table(table_name)

        the_exception = cm.exception
        self.assertEqual(
            str(the_exception),
            "'Invalid table name! No TABLE_TEST in DB!'")

    def test_get_stats(self):
        table_name = "SYSTEM_DataProviderInfo"
        stats = self.ii.get_stats(table_name)

        name = "'SYSTEM_DataProviderInfo'"
        unique = "[]"
        keys = "{'constrained_columns': ['ID_DataProvider'], 'name': 'PK_System_DataProviderInfo'}"
        foreign = "[]"
        columns = "[" + \
                r"{'name': 'ID_DataProvider', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': True, 'dialect_options': {'mssql_identity_start': 1, 'mssql_identity_increment': 1}}, " + \
                "{'name': 'Descrizione', 'type': NVARCHAR(length=255), 'nullable': True, 'default': None, 'autoincrement': False}, " + \
                "{'name': 'EndPoint', 'type': NVARCHAR(length=255), 'nullable': True, 'default': None, 'autoincrement': False}, " + \
                "{'name': 'UserID', 'type': NVARCHAR(length=50), 'nullable': True, 'default': None, 'autoincrement': False}, " + \
                "{'name': 'Password', 'type': NVARCHAR(length=50), 'nullable': True, 'default': None, 'autoincrement': False}, " + \
                "{'name': 'StoredProcedure', 'type': NVARCHAR(length=255), 'nullable': True, 'default': None, 'autoincrement': False}, " + \
                "{'name': 'ProviderAttivo', 'type': BIT(), 'nullable': True, 'default': None, 'autoincrement': False}" + \
            "]"
        response = f"Info(name={name}, unique={unique}, keys={keys}, foreign={foreign}, columns={columns})"

        self.assertEqual(response, str(stats))

    def tearDown(self):
        del self.ii


if __name__ == "__main__":
    main(verbosity=True)
