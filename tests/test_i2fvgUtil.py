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
        """
        Da un I2FVG.Info, ritorna una lista \
        con i nomi delle colonne presenti nella tabella.
        """
        default_column_names_list = [
            'col1', 'col2', 'col3', 'col4', 'col5'
        ]
        test_column_names_list = getColumnNames(self.info)
        self.assertListEqual(
            default_column_names_list,
            test_column_names_list,
            "Error for getColumnNames function"
        )
    
    def test_getColumnTypes(self):
        """
        Da un I2FVG.Info, ritorna una lista \
        con la tipologia delle colonne presenti nella tabella \
        con le strutture di dati di python.
        """
        default_column_types_list = [
            str, date, int, float, str
        ]
        test_column_types_list = getColumnTypes(self.info)
        self.assertListEqual(
            default_column_types_list,
            test_column_types_list,
            "Error for getColumnTypes function"
        )
    
    def test_getColumnLength(self):
        """
        Da un I2FVG.Info, ritorna una lista \
        con la lunghezza delle colonne presenti nella tabella \
        indicati dalle tipologie di dati in sqlalchemy.types
        """
        default_column_length_list = [
            11, None, None, None, 10
        ]
        test_column_length_list = getColumnLengths(self.info)
        self.assertListEqual(
            default_column_length_list,
            test_column_length_list,
            "Error for getColumnLengths"
        )

    def test_getColumnNullables(self):
        """
        Da un I2FVG.Info, ritorna una lista \
        con: 
            - True se la colonna può essere Null \
            - False se la colonna non può essere Null
        """
        default_column_nullable_list = [
            True, False, True, True, True
        ]
        test_column_nullable_list = getColumnNullables(self.info)
        self.assertListEqual(
            default_column_nullable_list,
            test_column_nullable_list,
            "Error for getColumnNullables"
        )

    def test_getColumnsInfo(self):
        # Because there's one column more from the db
        # that isn't into he data provider DataFrame
        default_selection = slice(0,-1) 
        default_column_names_list = [
            'col1', 'col2', 'col3', 'col4'
        ]
        default_column_types_list = [
            str, date, int, float
        ]
        default_column_length_list = [
            11, None, None, None
        ]
        default_column_nullable_list = [
            True, False, True, True
        ]
        
        info_col = getColumnsInfo(self.info, default_selection)
        
        with self.subTest():
            self.assertListEqual(
                default_column_names_list,
                info_col.names,
                "Column names are not the same"
            )
            self.assertListEqual(
                default_column_types_list,
                info_col.types,
                "Column types are not the same"
            )
            self.assertListEqual(
                default_column_length_list,
                info_col.lengths,
                "Column lengths are not the same"
            )
            self.assertListEqual(
                default_column_nullable_list,
                info_col.nullables,
                "Column nullables are not the same"
            )

    def test_getNumpyTypesConversion(self):
        """
        Test del metodo che converte una lista di \
        python types in una lista di numpy.dtypes
        """
        default_column_numpy_types_list = [
            np.dtype('i'), 
            np.dtype('float64'), 
            np.dtype('O'), 
            np.dtype('O'), 
        ]
        test_column_python_types_list = [
            int, float, object, date
        ]
        test_column_numpy_types_list = getNumpyTypesConversion(
            test_column_python_types_list
        )
        self.assertListEqual(
            default_column_numpy_types_list,
            test_column_numpy_types_list,
            "Data types are not the same"
        )