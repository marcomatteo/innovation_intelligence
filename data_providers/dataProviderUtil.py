"""
17/02/2020
"""

import pandas as pd
import numpy as np
from datetime import datetime

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

def getColumnNames(df: pd.DataFrame) -> list:
    """
    Funzione che da un pd.DataFrame ritorna \
    le colonne presenti in una lista
    """
    names_list = df.columns.to_numpy().tolist()
    return names_list

def getColumnsTypes(df: pd.DataFrame) -> list:
    """
    Funzione che da un pd.DataFrame ritorna \
    i tipi di dato del df in una lista
    """
    types_list = df.dtypes.to_numpy().tolist()
    return types_list

def getColumnsMaxLenght(df: pd.DataFrame) -> list:
    """
    Funzione che da un pd.DataFrame ritorna \
    le lunghezze massime per colonna del df \
    in una lista
    """
    
    def maxLenght(col) -> pd.Series:
        """Usiliary function for calculate column content lenght"""
        lenght = col.map(lambda x: len(str(x)))
        return lenght.max(axis=0)
    
    maxLenght_list = df.aggregate(maxLenght, axis=0).to_numpy().tolist()
    return maxLenght_list

def getColumnsNullPresence(df: pd.DataFrame) -> list:
    """
    Funzione che da un pd.DataFrame ritorna \
    una lista di bool indicante la presenza \
    di valori mancanti nelle colonne
    """
    
    def columnHaveNullValues(col) -> bool:
        """Usiliary function for check null presence in table columns"""
        answer_bool = col.isna().any()
        return answer_bool

    null_presence_list = df.aggregate(columnHaveNullValues, axis=0).to_numpy().tolist()
    return null_presence_list

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
