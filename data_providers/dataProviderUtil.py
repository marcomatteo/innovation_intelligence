"""
17/02/2020
"""

import pandas as pd
import numpy as np
from datetime import datetime

def getNumerateDictFromList(l: list) -> dict:
    return {i: val for i, val in enumerate(l)}

def getTrimmedLength(x) -> int:
    try:
        cond = np.isnan(x)
    except TypeError:
        cond = False # No Not a number

    if cond:
        return 0
    
    s = str(x).strip()
    return len(s)

def getMaxLength(col: pd.Series) -> pd.Series:
    """Usiliary function for calculate column content lenght"""
    length = col.map(lambda x: getTrimmedLength(x))
    return length.max(axis=0)

def ColumnHaveNullValues(col: pd.Series) -> bool:
    """Usiliary function for check null presence in table columns"""
    answer_bool = col.isna().any()
    return answer_bool

def formatFiscalcode(num: int) -> object:
    """
    Funzione per che formatta correttamente il codice fiscale 
    in formato stringa con gli zeri iniziali.
    """
    cf = str(num)
    while len(cf) < 11:
        cf = '0' + cf
    return cf

def formatFiscalcodeColumn(table: pd.DataFrame, col_name: object) -> pd.DataFrame:
    """
    Funzione che formatta correttamente la colonna del 
    codice fiscale in formato stringa con gli zeri iniziali.
    """
    if col_name not in table.columns:
        raise ValueError("Missing CF column in the table.")
    table.loc[:, col_name] = table[col_name].map(
        lambda x: formatFiscalcode(x)
    )
    return table

def isValidDateFormat(value, date_format: str) -> bool:
    """From a value return True if is a valid 
    date formatted string"""
    try:
        check = pd.isnull(value)
        if check:
            return True
    except:
        pass

    if isinstance(value, datetime):
        try:
            value = value.strftime(date_format)
        except:
            return False
    
    if value:
        x = str(value).strip()
        try:
            result = datetime.strptime(x, date_format)
        except:
            return False
    return True

def getBoolSeriesForDateChecking(s: pd.Series, date_format: str) -> pd.Series:
    try:
        result = s.map(lambda x: isValidDateFormat(x, date_format))
    except:
        return pd.Series([False], index=[0])
    return result.all()

# Exported

def getColumnNames(df: pd.DataFrame) -> dict:
    """
    Funzione che ritorna le colonne di un pd.DataFrame
    """
    names = df.columns.tolist()
    return getNumerateDictFromList(names)

def getColumnsTypes(df: pd.DataFrame) -> dict:
    """
    Funzione che ritorna i numpy.dtypes delle colonne di un pd.DataFrame
    """
    types_list = df.dtypes.tolist()
    return getNumerateDictFromList(types_list)

def getColumnsMaxLength(df: pd.DataFrame) -> dict:
    """
    Funzione che ritorna la lunghezza massima nelle colonne di un pd.DataFrame
    """    
    maxLength_list = df.aggregate(getMaxLength, axis=0).tolist()
    return getNumerateDictFromList(maxLength_list)

def getColumnNullables(df: pd.DataFrame) -> dict:
    """
    Funzione che da un pd.DataFrame ritorna 
    una lista di bool indicante la presenza 
    di valori mancanti nelle colonne
    """
    null_presence_list = df.aggregate(ColumnHaveNullValues, axis=0).tolist()
    return getNumerateDictFromList(null_presence_list)

# Deprecated
def getColumnsDateFormatted(column: str, date_format: str) -> (pd.Series, pd.Series):

    def getStringColumn(col) -> pd.Series:
        """Converto colonna in stringhe"""
        try:
            column_str = col.map(lambda x: str(x))
        except ValueError:
            return col    
        return column_str

    def getDateColumn(col) -> pd.Series:
        """Converto colonna in date secondo formattazione"""
        # Converto colonna in date formattate
        try:
            column_dates = col.map( 
                lambda x: 
                datetime.strptime(x, date_format)
            )
        except ValueError:
            return col
        return column_dates

    def getDateIntoStringColumn(col) -> pd.Series:
        """Converto colonna date in stringhe"""
        try:
            column_str = col.map(
                lambda x: x.strftime(date_format)
            )
        except ValueError:
            return col    
        return column_str

    column_str = getStringColumn(column)
    column_dates = getDateColumn(column_str)
    column_str_mod = getDateIntoStringColumn(column_dates)

    return column_str, column_str_mod
