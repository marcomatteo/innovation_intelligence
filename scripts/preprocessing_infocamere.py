# %% Setup
import sys
sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")
from data_providers import AnagraficaInfocamere

import numpy as np
import pandas as pd
import os
import dateutil
from datetime import datetime
# %% Parameters
file_name_full = "Infocamere2020.xlsx"
#%% Open file
anag = AnagraficaInfocamere(file_name_full) #TODO: da testare
# %% Utilizzo della funzione
df = anag.preprocessing_anagrafica()
# %% Output
path = r"C:/Users/buzzulini/OneDrive - Area Science Park"\
        + r"/Attività/Innovation Intelligence/Fonti/Infocamere/Datasets/"
with pd.ExcelWriter(path + file_name_full, date_format="DD/MM/YYYY", 
                    mode='a', engine="openpyxl") as writer:
    df.to_excel(
        writer,
        sheet_name="nFRIULI anagrafica",
        float_format="%.2f",
        index=False
    )