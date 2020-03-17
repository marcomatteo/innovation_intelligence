# %% Setup
import os
import sys
import pandas as pd
import numpy as np
sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")

# %% Load modules
import data_providers
import db_interface

# %% Load Bilanci interface
bil = db_interface.Bilanci()

# %% Query to the DB
cols = ['CF', 'Anno', 'TotaleAttivo', 'TotalePatrimonioNetto',
    'RapportoDiIndebitamento', 'RapportoDiIndebitamentoClasse']
query = "SELECT {} FROM {}".format(
    ",".join(cols), bil.tbl_info['bilancio'].name
)
bil.open_tables(query=query)

# %% RapportoDiIndebitamento functions definition
def calcRapportoDiIndebitamento(df: pd.DataFrame):
    cond1 = 'TotaleAttivo' in df.columns
    cond2 = 'TotalePatrimonioNetto' in df.columns
    if cond1 & cond2:
        return ((df['TotaleAttivo'] - df['TotalePatrimonioNetto']) / 
                            df['TotalePatrimonioNetto'] )
    else:
        data = [np.nan] * len(df.index)
        return pd.Series(data=data, index=df.index)

def getRapportoDiIndebitamento(df: pd.DataFrame):
    cond = 'RapportoDiIndebitamento' in df.columns
    if cond:
        return df.assign(
            calc_RDI = lambda df: calcRapportoDiIndebitamento(df)
        ).loc[:, ['RapportoDiIndebitamento', 'calc_RDI']]
    else:
        print("No RapportoDiIndebitamento in columns")

# %% Apply RapportoDiIndebitamento
index_check_df = getRapportoDiIndebitamento(bil.df)
index_check_df.replace(np.inf, np.nan, inplace=True)

# %% Quartili classi functions definition
def calcQuartili(s: pd.Series):
    classi = ['1. Basso', '2. Medio-basso', '3. Medio-alto', '4. Alto']
    return  pd.qcut(s, q=[0, .25, 0.5, 0.75, 1], labels=classi)

def getRapportoDiIndebitamentoClasse(df: pd.DataFrame):
    cond = 'RapportoDiIndebitamento' in df.columns
    if cond:
        cond = df['RapportoDiIndebitamento'].isna()
        grouped_column = df.loc[~ cond].groupby('Anno')['RapportoDiIndebitamento']
        quartiliRapportoDiIndebitamento = grouped_column.transform(
            lambda s: calcQuartili(s)
        ).rename("calc_RDIClasse")
        result = df.join(quartiliRapportoDiIndebitamento, how='left')
        cond = result['RapportoDiIndebitamento'].isna()
        result.loc[cond]["calc_RDIClasse"].astype('object').fillna("0. No data", inplace=True)
        return result   
    else:
        print("No RapportoDiIndebitamento in columns")

# %% Apply RapportoDiIndebitamentoClasse
classes_check_df = getRapportoDiIndebitamentoClasse(bil.df)

# %%
# TODO: effettuare il controllo e salvare un output