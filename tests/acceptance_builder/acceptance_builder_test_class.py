import unittest
from acceptance_builder import AcceptanceBuilder

class TestAcceptanceBuilderBaseClass(unittest.TestCase):
    
    maxDiff = None

    builder = NotImplemented    # type: AcceptanceBuilder
    column_lengths = NotImplemented # type: int

    def test_check_column_lengths(self):
        if (not self.builder is NotImplemented) & \
            (not self.column_lengths is NotImplemented):
            columns = self.builder.columns

            self.assertEqual(len(columns), self.column_lengths)
    
    def test_check_column_names(self):
        if (not self.builder is NotImplemented):
            exp_column_names = [c.nome for c in self.builder.columns]
            df_column_names = self.builder.dp.get_column_names()

            self.assertEqual(df_column_names, exp_column_names)
