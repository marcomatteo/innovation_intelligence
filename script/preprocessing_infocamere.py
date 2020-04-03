# %% Setup
import numpy as np
import pandas as pd
import os
import dateutil
from datetime import datetime
from data_providers import AnagraficaInfocamere
import sys

sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")
# %% Parameters
file_name_trim = "Infocamere2020_old"
file_name_full = file_name_trim + ".xlsx"
#%% Open file
anag = AnagraficaInfocamere(file_name_full) #TODO: da testare
# %% Utilizzo della funzione
df = anag.preprocessing_anagrafica()
# %% Output
df.to_excel(
    anag.file_path[:-5] + "_preprocessed.xlsx",
    sheet_name="FRIULI anagrafica",
    float_format="%.2f",
    index=False
)