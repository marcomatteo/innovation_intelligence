"""
Script di controllo per il Data Provider Finanziamenti FVG

necessità : controllo file fonte per presenza nuove leggi

TASK 2458:
1   Verifica elenco codice_legge nel workfolder "imprese"
2   verifica eventuale presenza nella tabella SVC_FinanziamentiUE_Schema
3   verifica eventuale presenza nel workfolder "progetti"
"""

# %% Setup
import pandas as pd
import numpy as np
import sys
import os

os.chdir("..")

# %% Librerie interne
from file_parser import ParserXls
from idb import DatabaseConnector

# %% Functions
def build_set_from_column(df: pd.DataFrame, pos: int) -> set:
    '''
    Return a set of elements from the column position in df
    '''
    col = df.columns[pos]
    return set(df[col].values)  

def get_set_differences(*args) -> set:
    '''
    Returns the set differences from multiple sets in args
    '''
    diff = set()
    for elements in args:
        if isinstance(elements, list):
            diff = get_set_differences(diff, *elements)
        if isinstance(elements, set):
            diff = elements.difference(diff)

    return diff

def get_laws_from_db() -> set:
    ''' 
    Returns the set of laws in DB from SVC_FinanziamentiUE_Schema
    '''
    # %% Database connection
    connector = DatabaseConnector()

    tbl_name = 'SVC_FinanziamentiUE_Schema'
    tbl_data = connector.get_dataframe_from_table(tbl_name)

    # %% Get set of data
    return build_set_from_column(tbl_data, 1)  

def get_dataframes_from_file(parser: ParserXls) -> list:
    '''
    Return a list of dataframes for an Excel file
    '''
    df_list = []
    for sheet_name in parser.get_sheet_names:
        df_list.append(parser.open_file(sheet_name=sheet_name))
    
    return df_list

def get_sets_from_dataframes(df_list: ParserXls) -> list:
    '''
    Return a list of dataframes for an Excel file
    '''
    # progetti, imprese = df_list[0], df_list[1]
    laws_for_sheets = []
    for df in df_list:
        laws_for_sheets.append(build_set_from_column(df, 0))
    
    return laws_for_sheets

def get_laws_from_file(file_name: str) -> set:
    '''
    Returns the set of laws in an Excel file from FinanziamentiFVG
    '''
    parser = ParserXls(file_name)

    # %% Open dataframes
    df_list = get_dataframes_from_file(parser)

    # %% Get the list of laws from each dataframe
    laws_for_sheets = get_sets_from_dataframes(df_list)

    # return get_set_differences(laws_for_sheets)
    return laws_for_sheets

# %% Data constants
FILES_PATH = r"./data/FinanziamentiFVG/2020/"
DB_LAWS = get_laws_from_db()
NOT_FOUNDED = set()

# %% File names
for _, _, file_names in os.walk(FILES_PATH):
    pass

# %% Get the 
laws_not_in_progetti = []
for file_name in file_names:
    laws_not_in_progetti.append(get_laws_from_file(FILES_PATH + file_name))

# %%
NOT_FOUNDED = get_set_differences(DB_LAWS, laws_not_in_progetti)

# %%
NOT_FOUNDED

# %%
