from datetime import datetime
from unittest.mock import MagicMock
import numpy as np
import pandas as pd
from data_provider.data_provider import DataProvider

from unittest import TestCase
from acceptance_builder import AcceptanceBuilder


class TestAcceptanceBuilder(TestCase):

    @classmethod
    def setUpClass(cls):
        data = {
            'col1': ['00993883991', '00993884492', '00912383993', '00233883994'],
            'col2': ['UD', 'PN', 'TS', 'GO'],
            'col3': [0, 1, 1, 1],
            'col4': ([np.nan] * 3) + [0.24],
            'col5': pd.date_range(start=datetime.today(), periods=4)
        }
        df = pd.DataFrame(data)
        col_types = {0: 'object', 1: 'object', 2: 'int', 3: 'float', 4: 'date'}
        col_constraints = {0: False, 1: False, 2: True, 3: False, 4: False}
        cls.dp = DataProvider(df, col_types, col_constraints)

        cls.columns = [
            AcceptanceBuilder.Columns(nome='fiscalcode',
                                      tipologia=np.dtype('O'),
                                      lunghezza=19, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='pv',
                                      tipologia=np.dtype('O'),
                                      lunghezza=2, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='sedeul',
                                      tipologia=np.dtype('int64'),
                                      lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='id_istat_province',
                                      tipologia=np.dtype('float64'),
                                      lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='istat_province_prcode',
                                      tipologia=np.dtype('<M8[ns]'),
                                      lunghezza=2, nullable=True, pk=False)
        ]

        cls.builder = AcceptanceBuilder(
            dp=cls.dp, dp_file_extension='csv', columns=cls.columns)

    def setUp(self) -> None:
        self.builder = AcceptanceBuilder(dp=self.dp, dp_file_extension='csv',
                                         columns=self.columns)

    def test_check_file_extension(self):
        self.builder.dp = MagicMock()
        self.builder.dp.file_parser.file_ext = 'csv'
        self.assertEqual(self.builder.check_file_extension(), 'csv')

    def test_check_column_number(self):
        self.builder.dp = MagicMock()
        self.builder.dp.get_column_number.return_value = 5
        self.assertEqual(self.builder.check_column_number(), 5)

    def test_check_column_types(self):
        self.assertEqual(self.builder.check_column_types(),
                         [np.dtype('O'),
                          np.dtype('O'),
                          np.dtype('int64'),
                          np.dtype('float64'),
                          np.dtype('<M8[ns]')])

    def test_check_column_length(self):
        self.assertEqual(self.builder.check_column_length(),
                         [11, 2, 1, 4, 26])

    def test_check_column_nullables(self):
        self.assertEqual(self.builder.check_column_nullables(),
                        [False, False, False, True, False])

    def test_check_column_constraints(self):
        self.assertEqual(self.builder.check_column_constraints(), 2)


if __name__ == '__main__':
    from unittest import main
    main(verbosity=2)
