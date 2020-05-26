"""
Script di preparazione al controllo importazione dati PATSTAT da file excel da Priore
"""
# %% Setup
from file_parser import ParserXls
from idb import DatabaseConnector

import pandas as pd
import numpy as np
import os

# %% Change directory
os.chdir("..")

# %% Apro tabella del matching per incrociare l'id con i CF
db = DatabaseConnector()
imprese_match = db.get_dataframe_from_table("SVC_Imprese_Match")

# %% Apro file brevetti
file_fonte_name = r"data/PATSTAT/2020_05_12_brevetti.xlsx"

file_fonte = ParserXls(file_fonte_name)
file_fonte_df = file_fonte.open_file(sheet_name=0)

# %% Incrocio i dati per ottenere il Codice fiscale nel file fonte
file_fonte_df = file_fonte_df.astype({"idimpresa": "int64"}).rename(
    columns={"idimpresa": "IDEsterno"})

merged_df = file_fonte_df.merge(imprese_match, on="IDEsterno", how="left")

# %% Salvo il file con i soli match
merged_df.dropna(subset=["CF"]).to_excel(
    r"data/PATSTAT/2020_05_12_brevetti_da_testare.xlsx", index=False)

# Lavoro restante: controllo a campione su 10 brevetti
