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

    def test_dataframe_index_differences_defaultIndex(self):
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

    def test_dataframe_index_differences_labelIndex(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        labels = ['a', 'b', 'c']

        df1 = pd.DataFrame(data, index=labels)
        df2 = pd.DataFrame(data, index=labels)
        df_check = dataframe_index_differences(df1, df2)
        self.assertTrue(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )

    def test_dataframe_index_differences_numericalIndex(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        nums = [1, 2, 3]

        df1 = pd.DataFrame(data, index=nums)
        df2 = pd.DataFrame(data, index=nums)
        df_check = dataframe_index_differences(df1, df2)
        self.assertTrue(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )

    def test_dataframe_index_differences_multiIndex(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        labels = [['a', 'b', 'c'],
                    ['d', 'e', 'f']]

        tuples = list(zip(*labels)) # * means flatten array

        index = pd.MultiIndex.from_tuples(tuples, 
                        names=['first','second'])

        df1 = pd.DataFrame(data, index=index)
        df2 = pd.DataFrame(data, index=index)
        df_check = dataframe_index_differences(df1, df2)
        self.assertTrue(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )

    def test_dataframe_index_differences_WrongLabelIndex(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        labels1 = ['a', 'b', 'c']
        labels2 = ['a', 'b', 'f']

        df1 = pd.DataFrame(data, index=labels1)
        df2 = pd.DataFrame(data, index=labels2)
        df_check = dataframe_index_differences(df1, df2)
        self.assertFalse(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )

    def test_dataframe_index_differences_WrongNumericalIndex(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        nums1 = [1, 2, 3]
        nums2 = [1, 5, 3]

        df1 = pd.DataFrame(data, index=nums1)
        df2 = pd.DataFrame(data, index=nums2)
        df_check = dataframe_index_differences(df1, df2)
        self.assertFalse(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )

    def test_dataframe_index_differences_WrongMultiIndex(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        labels1 = ['a', 'b', 'c']
        labels1_mod = ['a', 'b', 'f']
        labels2 = ['d', 'e', 'f']

        tuples1 = list(zip(labels1, labels2)) 
        tuples2 = list(zip(labels1_mod, labels2)) 

        index1 = pd.MultiIndex.from_tuples(tuples1, 
                        names=['first','second'])
        index2 = pd.MultiIndex.from_tuples(tuples2, 
                        names=['first','second'])

        df1 = pd.DataFrame(data, index=index1)
        df2 = pd.DataFrame(data, index=index2)
        df_check = dataframe_index_differences(df1, df2)
        self.assertFalse(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )
    
    def test_dataframe_index_differences_WrongLabelIndex_leftJoin(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        labels1 = ['a', 'b', 'c']
        labels2 = ['a', 'b', 'f']

        df1 = pd.DataFrame(data, index=labels1)
        df2 = pd.DataFrame(data, index=labels2)
        df_check = dataframe_index_differences(df1, df2, 'left')
        self.assertFalse(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )
        
    def test_dataframe_index_differences_WrongNumericalIndex_leftJoin(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        nums1 = [1, 2, 3]
        nums2 = [1, 5, 3]

        df1 = pd.DataFrame(data, index=nums1)
        df2 = pd.DataFrame(data, index=nums2)
        df_check = dataframe_index_differences(df1, df2, 'left')
        self.assertFalse(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )

    def test_dataframe_index_differences_WrongMultiIndex_leftJoin(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        labels1 = ['a', 'b', 'c']
        labels1_mod = ['a', 'b', 'f']
        labels2 = ['d', 'e', 'f']

        tuples1 = list(zip(labels1, labels2)) 
        tuples2 = list(zip(labels1_mod, labels2)) 

        index1 = pd.MultiIndex.from_tuples(tuples1, 
                        names=['first','second'])
        index2 = pd.MultiIndex.from_tuples(tuples2, 
                        names=['first','second'])

        df1 = pd.DataFrame(data, index=index1)
        df2 = pd.DataFrame(data, index=index2)
        df_check = dataframe_index_differences(df1, df2, 'left')
        self.assertFalse(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )

    def test_dataframe_index_differences_WrongLabelIndex_rightJoin(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        labels1 = ['a', 'b', 'c']
        labels2 = ['a', 'b', 'f']

        df1 = pd.DataFrame(data, index=labels1)
        df2 = pd.DataFrame(data, index=labels2)
        df_check = dataframe_index_differences(df1, df2, 'right')
        self.assertFalse(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )

    def test_dataframe_index_differences_WrongNumericalIndex_rightJoin(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        nums1 = [1, 2, 3]
        nums2 = [1, 5, 3]

        df1 = pd.DataFrame(data, index=nums1)
        df2 = pd.DataFrame(data, index=nums2)
        df_check = dataframe_index_differences(df1, df2, 'right')
        self.assertFalse(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )

    def test_dataframe_index_differences_WrongMultiIndex_rightJoin(self):
        data = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3],
            'col3': [0.5, 0.04, 0.99]
        }
        labels1 = ['a', 'b', 'c']
        labels1_mod = ['a', 'b', 'f']
        labels2 = ['d', 'e', 'f']

        tuples1 = list(zip(labels1, labels2)) 
        tuples2 = list(zip(labels1_mod, labels2)) 

        index1 = pd.MultiIndex.from_tuples(tuples1, 
                        names=['first','second'])
        index2 = pd.MultiIndex.from_tuples(tuples2, 
                        names=['first','second'])

        df1 = pd.DataFrame(data, index=index1)
        df2 = pd.DataFrame(data, index=index2)
        df_check = dataframe_index_differences(df1, df2, 'right')
        self.assertFalse(
            df_check.empty,
            "Il DataFrame dev'essere vuoto perché i DataFrames comparati sono uguali"
        )

if __name__ == '__main__':
    loader = test.TestLoader()
    suite = loader.loadTestsFromTestCase(Test_CertificateUtilities)
    runner = LogCaptureRunner(verbosity=2)
    runner.run(suite)
