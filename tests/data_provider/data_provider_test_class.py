from unittest.case import skip
from data_provider import DataProvider
from file_parser import IParser

import unittest
import pandas as pd

class TestDataProviderBaseClass(unittest.TestCase):

    maxDiff = None

    dp = NotImplemented # type: DataProvider
    columns = NotImplemented    # type: list[str]
    file_path = NotImplemented  # type: str
    first_row = NotImplemented  # type: list
    file_parser = NotImplemented    # type: IParser
    column_types = NotImplemented   # type: dict
    column_constraints = NotImplemented # type: dict
    file_parser_separator = NotImplemented  # type: str
    file_parser_sheet_name = NotImplemented # type: str

    def test_matching_columns_names(self):
        if ((not self.columns is NotImplemented) and
            (not self.dp is NotImplemented)):
            self.assertEqual(self.columns, self.dp.get_column_names())

    def test_first_row_matching(self):
        if ((not self.first_row is NotImplemented) and
            (not self.dp is NotImplemented)):
            self.assertEqual(self.first_row,
                                self.dp.df.iloc[0,:].tolist())

    def test_class_inheritance_from_data_provider(self):
        if not self.dp is NotImplemented:
            self.assertTrue(issubclass(type(self.dp), DataProvider))

    def test_attributes_isinstance_df(self):
        if not self.dp is NotImplemented:
            self.assertTrue(isinstance(self.dp.df, pd.DataFrame))

    def test_attributes_isinstance_file_parser(self):
        if ((not self.file_parser_separator is NotImplemented) and
            (not self.dp is NotImplemented)):
            self.assertTrue(isinstance(self.dp.file_parser,
                                            self.file_parser))        

    def test_attributes_file_path(self):
        if ((not self.file_path is NotImplemented) and
            (not self.dp is NotImplemented)):
            self.assertTrue(isinstance(self.dp.file_path, str))
            self.assertEqual(self.file_path, self.dp.file_path)

    def test_attributes_file_parser_separator(self):
        if ((not self.file_parser_separator is NotImplemented) and
            (not self.dp is NotImplemented)):
            self.assertTrue(isinstance(self.dp.file_parser_sep, str))
            self.assertEqual(self.file_parser_separator,
                                self.dp.file_parser_sep)

    @skip
    def test_attributes_column_types(self):
        if ((not self.column_types is NotImplemented) and
            (not self.dp is NotImplemented)):
            self.assertTrue(isinstance(self.dp.column_types, dict))
            self.assertEqual(self.column_types, self.dp.column_types)

    @skip
    def test_attributes_column_constraints(self):
        if ((not self.column_constraints is NotImplemented) and
            (not self.dp is NotImplemented)):
            self.assertTrue(isinstance(self.dp.column_constraints, dict))
            self.assertEqual(self.column_constraints, 
                                self.dp.column_constraints)
