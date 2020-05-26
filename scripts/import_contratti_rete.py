"""
Script per controllo importazione dei Contratti di Rete
"""
# %% Setup
from data_provider import ContrattiRete
from idb import DatabaseConnector

import pandas as pd
import numpy as np
import os

# %% Cambio directory
os.chdir("..")

# %% Apro file fonte
dataprovider_df = ContrattiRete().df

# %% Leggo il DB
db = DatabaseConnector()
database_df = db.get_dataframe_from_table("DATA_ContrattiRete")

# %% Elimino NESSUN CONTRATTO
database_df.dropna(subset=["SoggettoGiuridico"], inplace=True)

# %% Ottengo lista di CF di I2FVG per controllare l'importazione
cf_df = db.get_dataframe_from_query("SELECT DISTINCT CF FROM DATA_Impresa")

cf_list = cf_df["CF"].tolist()

# %% Filtro il Data Provider con i codici fiscali
cf_filter = dataprovider_df["c.f."].isin(cf_list)
dataprovider_only_cf_i2fvg = dataprovider_df.loc[cf_filter]

# %% Join tra i dataframes
dataprovider_keys = ["numero repertorio", "numero atto", "c.f."]
database_keys = ["NumeroRepertorio", "NumeroAtto", "CF"]

db_to_join = database_df.set_index(database_keys)

dp_to_join = dataprovider_df.set_index(dataprovider_keys)
dp_to_join.index.set_names(database_keys, inplace=True)

df_join = db_to_join.join(dp_to_join, lsuffix="_DB", rsuffix="_DP")

# %% Check
isna_check = df_join["denominazione contratto"].isna()

if isna_check.any():
    print("Ci sono dei contratti che non sono stati importati.")
else:
    print("Tutti i contratti sono stati importati.")

# %%
