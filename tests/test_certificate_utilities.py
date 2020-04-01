import sys
import logging
import unittest as test
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")

from certificates import dataframe_index_differences
from log_test import LogCaptureRunner, BaseTestCase

class Test_CertificateUtilities(BaseTestCase):

    def test_dataframe_index_differences_equals(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        df1 = pd.DataFrame(data)
        df2 = pd.DataFrame(data)
        df_check = dataframe_index_differences(df1, df2)
        self.assertTrue(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )


if __name__ == '__main__':
    loader = test.TestLoader()
    suite = loader.loadTestsFromTestCase(Test_CertificateUtilities)
    runner = LogCaptureRunner(verbosity=2)
    runner.run(suite)
