"""
Modulo che contiene funzioni utili per certificare efficacemente
e in modo esaustivo le US di Innovation Intelligence
"""
import pandas as pd
import numpy as np

def dataframe_index_differences(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    left_index_levels = df1.index.nlevels
    right_index_levels = df2.index.nlevels

    # Check if indexes have the same shape
    if left_index_levels != right_index_levels:
        raise ValueError("DataFrames have different index shape!")
    
    # Rename indici per il join
    names = ['idx_' + str(i) for i in range(left_index_levels)]
    df1.index.set_names(names, inplace = True)
    df2.index.set_names(names, inplace = True)

    df_join = df1.join(
            df2,
            how = "outer",
            lsuffix="_left",
            rsuffix="_right"
        )
    
    check = df_join.isnull().any(axis=1)

    return df_join.loc[check]
