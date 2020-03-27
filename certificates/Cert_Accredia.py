# %% Setup
import sys
import os
import pandas as pd
sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")
# %% Load Data Provider and DB interface
from data_providers import Accredia
from db_interface import Certificazione
from db_interface import I2FVG
# %% Carico file fonte
data_provider = Accredia("20200203_accredia.csv")
data_provider_df = data_provider.get_renamed_df()
print(data_provider_df.info())
data_provider_df.head()
# %% Estraggo lista dei CF univoci presenti nel DB
ii = I2FVG()
cf_list = pd.read_sql_query(
    "SELECT DISTINCT CF FROM DATA_Impresa", ii.engine)['CF'].tolist()
# %% Incrocio con il file fonte per ottenere la lista di certificazioni
cond_selection_cfs = data_provider_df['CF'].isin(cf_list)
data_provider_df_selected = data_provider.df.loc[cond_selection_cfs]
print(data_provider_df_selected.info())
data_provider_df_selected.head()
# %% Carico informazioni dal DB sulle Certificazioni
db_obj = Certificazione()
db_df = db_obj.df
print(db_df.info())
db_df.head()
# %%
