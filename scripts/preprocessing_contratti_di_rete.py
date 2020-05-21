#!/usr/bin/env python.
# %% Setup
import sys
import os
os.chdir(r"../")

ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)

from data_provider import ContrattiRete
import pandas as pd
# %% Open File

contratti = ContrattiRete(inTest=False)


# %%

from idb import Anagrafica

cf_list = Anagrafica().get_fiscalcode_list()

# %%
# %%

contratti.set_filtred_fiscal_codes_dataframe(cf_column=7)

# %% Find duplicates

print(contratti.is_valid_data_provider())

# %%
duplicati = contratti.get_duplicates()

# %%
