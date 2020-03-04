import pandas as pd
import numpy as np
from datetime import datetime
from db_interface import I2FVG

def getColumnNames(info: I2FVG.Info) -> list:
    """
    Metodo che dato un oggetto info ritorna la \
    lista con i nomi delle colonne presenti nella tabella.
    """
    result = list()
    for col in info.columns:
        name = col['name']
        result.append(name)
    return result

def getColumnTypes(info: I2FVG.Info) -> list:
    """
    Metodo che dato un oggetto info ritorna la \
    lista delle tipologie delle colonne presenti nella tabella.
    """
    result = list()
    for col in info.columns:
        col_type = col['type']
        try:
            ty = col_type.python_type
        except NotImplementedError:
            ty = object
        result.append(ty)
    return result

def getNumpyTypesConversion(py_types: list) -> list:
    """
    Metodo che data una lista di Python types \
    ritorna una lista di Numpy.dtypes
    """
    result = [
        np.dtype(ty)
        for ty in py_types
    ]
    return result

def getColumnLengths(info: I2FVG.Info) -> list:
    """
    Metodo che dato un oggetto info ritorna la \
    lista delle lunghezze massime delle colonne \
    presenti nella tabella.
    """
    result = list()
    for col in info.columns:
        try:
            length = col['type'].length
        except:
            length = None
        result.append(length)    
    return result

def getColumnNullables(info: I2FVG.Info) -> list:
    """
    Metodo che dato un oggetto info ritorna la \
    lista con un bool indicante delle colonne presenti \
    nella tabella possono essere o non essere Null: \
        - True: il campo può essere Null
        - False: il campo non può essere Null 
    """
    result = list()
    for col in info.columns:
        nullable = col['nullable']
        result.append(nullable)
    return result

def getColumnsInfo(info: I2FVG.Info, sel: slice=None) -> I2FVG.InfoCols:
    name_list = getColumnNames(info)
    type_list = getColumnTypes(info)
    length_list = getColumnLengths(info)
    nullable_list = getColumnNullables(info)
    if not sel:
        sel = slice(None)
    info_col = I2FVG.InfoCols(
        names=name_list[sel],
        types=type_list[sel],
        lengths=length_list[sel],
        nullables=nullable_list[sel]
    )

    return info_col

