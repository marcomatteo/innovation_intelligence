import unittest as test
import pandas as pd
import numpy as np

from datetime import date
from sqlalchemy import types

from db_interface import I2FVG
from db_interface import (
    getColumnsInfo, getColumnLengths,
    getColumnNames, getColumnNullables,
    getColumnTypes, getNumpyTypesConversion
)
from db_interface.i2fvgUtil import (
    TypeReplacing
)

class Test_i2fvgUtil(test.TestCase):
    
    @classmethod
    def setUpClass(cls):
        col1 = {
            'name': 'col1',
            'type': types.VARCHAR(length=11),
            'nullable': True,
            'default': None
        }
        col2 = {
            'name': 'col2',
            'type': types.DATE(),
            'nullable': False,
            'default': None
        }
        col3 = {
            'name': 'col3',
            'type': types.INTEGER(),
            'nullable': True,
            'default': None
        }
        col4 = {
            'name': 'col4',
            'type': types.FLOAT(),
            'nullable': True,
            'default': None
        }
        col5 = {
            'name': 'col5',
            'type': types.CHAR(length=10, collation='Latin1_General_CI_AS'),
            'nullable': True,
            'default': None
        }
        cols = [col1, col2, col3, col4, col5]
        cls.info = I2FVG.Info(
            name='tbl_prova',
            unique=['pk1', 'pk2'],
            keys=[],
            foreign=[],
            columns=cols    
        )

    def test_getColumnNames(self):
        test_column_names_list = getColumnNames(self.info)
        self.assertDictEqual(
            test_column_names_list,
            { 0: 'col1', 1: 'col2', 2: 'col3', 3: 'col4', 4: 'col5' },
            "Column names must be 0: 'col1', 1: 'col2', 2: 'col3', 3: 'col4', 4: 'col5'"
        )
    
    def test_getColumnTypes(self):
        test_column_types = getColumnTypes(self.info)
        self.assertDictEqual(
            test_column_types,
            { 0: str, 1: date, 2: int, 3: float, 4: str },
            "Types must be -> 0: str, 1: date, 2: int, 3: float, 4: str"
        )
    
    def test_getColumnLength(self):
        test_column_length = getColumnLengths(self.info)
        self.assertDictEqual(
            test_column_length,
            { 0: 11, 1: None, 2: None, 3: None, 4: 10 },
            "Dict of length must be 0: 11, 1: None, 2: None, 3: None, 4: 10"
        )

    def test_getColumnNullables(self):
        test_column_nullable = getColumnNullables(self.info)
        self.assertDictEqual(
            test_column_nullable,
            { 0: True, 1: False, 2: True, 3: True, 4: True },
            "Dict must be 0: True, 1: False, 2: True, 3: True, 4: True"
        )

    def test_getColumnsInfo(self):
        # Because there's one column more from the db
        # that isn't into he data provider DataFrame
        default_selection = slice(0,-1)  
        info_col = getColumnsInfo(self.info, default_selection)
        
        with self.subTest():
            self.assertListEqual(
                info_col.names,
                ['col1', 'col2', 'col3', 'col4'],
                "Column names are not the same"
            )
            self.assertListEqual(
                info_col.types,
                [str, date, int, float],
                "Column types are not the same"
            )
            self.assertListEqual(
                info_col.lengths,
                [11, None, None, None],
                "Column lengths are not the same"
            )
            self.assertListEqual(
                info_col.nullables,
                [True, False, True, True],
                "Column nullables are not the same"
            )

    def test_getNumpyTypesConversion(self):
        test_column_python_types_list = [
            int, float, object, date, str
        ]
        test_column_numpy_types = getNumpyTypesConversion(
            test_column_python_types_list
        )
        self.assertDictEqual(
            test_column_numpy_types,
            {0: np.dtype('int32'), 
            1: np.dtype('float64'), 
            2: np.dtype('O'), 
            3: np.dtype('datetime64[ns]'), 
            4: np.dtype('O')},
            "Data types are not the same"
        )

    def test_TypeReplacing_String(self):
        value = str
        self.assertEqual(
            TypeReplacing(value), 
            object, 
            "Type str -> object"
        )
    
    def test_TypeReplacing_Date(self):
        value = date
        self.assertEqual(
            TypeReplacing(value), 
            '<M8[ns]', 
            "Type date -> '<M8[ns]'"
        )
    
    def test_TypeReplacing_Int(self):
        value = int
        self.assertEqual(
            TypeReplacing(value), 
            int, 
            "Type int -> int"
        )

    def test_TypeReplacing_Float(self):
        value = float
        self.assertEqual(
            TypeReplacing(value), 
            float, 
            "Type float -> float"
        )