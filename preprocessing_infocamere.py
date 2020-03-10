# %% Setup
import numpy as np
import pandas as pd
import os
import dateutil

PATH = r"C:/Users/buzzulini/Desktop/"
file_name = "Tracciato dati Infocamere_I2FVG 2mar2020.xlsx"

#%% Open file
df = pd.read_excel(PATH + file_name, sheet_name=0, dtype=object, date_parser=dateutil.parser.parser("%d/%m/%Y"))

# %% Preprocessing
cess_artigiana_col = "cessazione artigiana"
to_change_cols = [
    "N-ALBO-AA - Numero di iscrizione all'Albo Imprese Artigiane",
    "DT-ISCR-AA - Data di iscrizione all'Albo delle Imprese Artigiane"
]
if cess_artigiana_col in df.columns:
    cond = df.loc[:, cess_artigiana_col].notnull()
    df.loc[cond, to_change_cols] = np.nan
    df.drop(columns=cess_artigiana_col, inplace=True)
    
# %% Output
df.to_excel(PATH + "AnagraficaPreprocessed.xlsx")
