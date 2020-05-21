"""
File per la certificazione di Modefinance 2020
"""

# %% Setup
from data_provider import BrevettiIta
from idb import InnovationIntelligence
from idb import DatabaseConnector

import os
import pandas as pd
import numpy as np

os.chdir("..")

# %% Function


def clean_columns(column):
    return column.map(lambda x: str(x).strip())


# %% Open Brevetti
data_provider = BrevettiIta()

# %% Seleziono solo alcuni cf presenti in anagrafica
data_provider.set_filtred_fiscal_codes_dataframe(cf_column=5)
# %% Controllo a campione sui seguenti brevetti
data_provider.df.loc[data_provider.df["DATA_DEPOSITO"].dt.year == 2018].sample(
    n=5)
    
# %% Controllo a campione sui seguenti brevetti
data_provider.df.loc[data_provider.df["DATA_DEPOSITO"].dt.year == 2017].sample(
    n=5)
