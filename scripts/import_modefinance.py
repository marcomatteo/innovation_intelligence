"""
File per la certificazione di Modefinance 2020
"""

# %% Setup
from data_provider import Modefinance
from idb import InnovationIntelligence
from idb import DatabaseConnector

import os
import pandas as pd
import numpy as np

os.chdir("..")
last_year = 2019

# %% Function definition


def preprocessing_modefinance_data_provider(data_provider: Modefinance) -> pd.DataFrame:

    def get_anno(value):
        if len(value) == 0:
            return ""
        else:
            return str(value)[6:]

    df = data_provider.df.copy()

    df["Anno"] = df["evaluation_date"].map(lambda val: get_anno(val))
    df.drop(columns="evaluation_date", inplace=True)

    df.rename(columns={'fiscal_code': 'CF',
                       'final_rank': 'MoreClass'}, inplace=True)

    result = df.astype({'Anno': 'float64', 'MoreClass': 'float64'}) \
        .set_index(["CF", "Anno"])["MoreClass"]

    return result.to_frame()


def clean_columns(column):
    return column.map(lambda x: str(x).strip())


# %% Open Modefinance
data_provider = Modefinance()

# %% Seleziono solo alcuni cf presenti in anagrafica
data_provider.set_filtred_fiscal_codes_dataframe(cf_column=0)

# %% Open Database
QUERY = """
        SELECT CF, Anno, MoreClass FROM DATA_Rating
        """
tbl_rating = pd.read_sql_query(
    QUERY, con=DatabaseConnector().connection_string) \
    .apply(lambda col: clean_columns(col)) \
    .astype({'Anno': 'float64', 'MoreClass': 'float64'})

tbl_rating.dropna(inplace=True)

# %% Preparazione dataframes
df_dataProvider = preprocessing_modefinance_data_provider(data_provider)
df_database = tbl_rating.set_index(["CF", "Anno"])

# %% Unione dei dataframes
df_join = df_dataProvider.join(
    df_database, how='left', lsuffix='dp', rsuffix='db').reset_index()

# %%
df_join.loc[df_join['Anno'] == last_year].info()
print("Non ci sono rating importati non correttamente: ",
      df_join.loc[df_join['Anno'] == last_year].query("MoreClassdp != MoreClassdb").empty)

# %%


# %%
