"""
Modulo che contiene funzioni utili per certificare efficacemente
e in modo esaustivo le US di Innovation Intelligence
"""
import pandas as pd
import numpy as np
import warnings

def trim_cols(col):
    """Elimina gli spazi prima e dopo in ogni riga della colonna col"""
    warnings.warn("Use trim_columns_spaces()")
    return col.map(lambda x: str(x).strip())

def trim_columns_spaces(col):
    """Elimina gli spazi prima e dopo in ogni riga della colonna col"""
    return col.map(lambda x: str(x).strip())

def dataframe_index_differences(df1: pd.DataFrame, df2: pd.DataFrame, how='outer') -> pd.DataFrame:
    """
    Funzione che controlla se gli indici di due DataFrame
    corrispondono e sono uguali
    """
    types_join = ['inner', 'left', 'right', 'left', 'outer']
    if how not in types_join:
        raise AttributeError("Invalid type of join")

    left_index_levels = df1.index.nlevels
    right_index_levels = df2.index.nlevels

    # Check if indexes have the same shape
    if left_index_levels != right_index_levels:
        raise ValueError("DataFrames have different index shape")
    
    # Rename indici per il join
    names = ['idx_' + str(i) for i in range(left_index_levels)]
    df1.index.set_names(names, inplace = True)
    df2.index.set_names(names, inplace = True)

    df_join = df1.join(
            df2,
            how = how,
            lsuffix="_left",
            rsuffix="_right"
        )

    check = df_join.isnull().any(axis=1)

    return df_join.loc[check]
