import pandas as pd
import numpy as np
from datetime import datetime, date
from db_interface import I2FVG

def TypeReplacing(ty):
    """
    Metodo per il mapping delle tipologie 
    del DB convertite in Python type 
    per le tipologie problematiche
    """  
    if ty is str:
        return object
    if ty is date:
        return '<M8[ns]'
    return ty

def getColumnNames(info: I2FVG.Info) -> dict:
    """
    Metodo che dato un oggetto info ritorna
    i nomi delle colonne presenti nella tabella.
    """
    result = dict()
    for i, col in enumerate(info.columns):
        result[i] = col['name']
    return result

def getColumnTypes(info: I2FVG.Info) -> dict:
    """
    Metodo che dato un oggetto info ritorna la 
    tipologie delle colonne presenti nella tabella.
    """
    result = dict()
    for i, col in enumerate(info.columns):
        col_type = col['type']
        try:
            ty = col_type.python_type
        except NotImplementedError:
            ty = object
        result[i] = ty
    return result

def getNumpyTypesConversion(py_types: list) -> dict:
    """
    Metodo che data una lista di Python types
    ritorna una lista di Numpy.dtypes
    """
    py_types_mapped = map(TypeReplacing, py_types)
    result = {
        i: np.dtype(ty)
        for i,ty in enumerate(py_types_mapped)
    }
    return result

def getColumnLengths(info: I2FVG.Info) -> dict:
    """
    Metodo che dato un oggetto info ritorna la 
    le lunghezze massime delle colonne 
    presenti nella tabella.
    """
    result = dict()
    for i, col in enumerate(info.columns):
        try:
            length = col['type'].length
        except:
            length = None
        result[i] = length    
    return result

def getColumnNullables(info: I2FVG.Info) -> dict:
    """
    Metodo che dato un oggetto info ritorna la 
    lista con un bool indicante delle colonne presenti 
    nella tabella possono essere o non essere Null: 

        - True: il campo può essere Null

        - False: il campo non può essere Null 
    """
    result = dict()
    for i,col in enumerate(info.columns):
        nullable = col['nullable']
        result[i] = nullable
    return result

def getColumnsInfo(info: I2FVG.Info, sel: slice=None) -> I2FVG.InfoCols:
    name_list = getColumnNames(info)
    type_list = getColumnTypes(info)
    length_list = getColumnLengths(info)
    nullable_list = getColumnNullables(info)

    if not sel:
        sel = slice(None)

    info_col = I2FVG.InfoCols(
        names=list(name_list.values())[sel],
        types=list(type_list.values())[sel],
        lengths=list(length_list.values())[sel],
        nullables=list(nullable_list.values())[sel]
    )

    return info_col

