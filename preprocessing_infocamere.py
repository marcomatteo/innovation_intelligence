# %% Setup
import numpy as np
import pandas as pd
import os
import dateutil
from datetime import datetime
from data_providers import AnagraficaInfocamere
# %% Parameters
PATH = r"C:/Users/buzzulini/OneDrive - Area Science Park/Attività/Innovation Intelligence/Fonti/Infocamere/Datasets/"
file_name_trim = "Infocamere2020"
file_name_full = file_name_trim + ".xlsx"
#%% Open file
#df = pd.read_excel(PATH + file_name + ".xlsx", sheet_name=0, dtype=object, date_parser=dateutil.parser.parser("%d/%m/%Y"))
anag = AnagraficaInfocamere(file_name_full)
# %% View the dataset
cess_artigiana_col = "Cessazione artigiana"
to_change_cols = [
    "N-ALBO-AA - Numero di iscrizione all'Albo Imprese Artigiane",
    "DT-ISCR-AA - Data di iscrizione all'Albo delle Imprese Artigiane"
]
df = anag.df.copy()
print("Campi originali:\n")
df.loc[:, to_change_cols + [cess_artigiana_col]].info()
# %% Preprocessing
if cess_artigiana_col in df.columns:
    cond = df[cess_artigiana_col].notna()
    df.loc[cond, to_change_cols] = np.nan
print("Pulizia campi impresa Artigiana effettuata.\n")
df.loc[:, to_change_cols + [cess_artigiana_col]].info()
# %% Drop column cess_artigiana_col
df.drop(columns=cess_artigiana_col, inplace=True)
print("\nEliminazione colonna {} effettuata.".format(cess_artigiana_col))
# %% Output
df.to_excel(
    PATH + file_name_trim + "_preprocessed.xlsx",
    sheet_name="FRIULI anagrafica",
    float_format="%.2f",
    index=False
)
