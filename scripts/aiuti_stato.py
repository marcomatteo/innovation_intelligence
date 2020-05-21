"""
Prova del parser XML per mandare il file funzionante ad Alessio
"""
# %% Setup

from file_parser import AiutiDiStato, XMLParser

import os
os.chdir("..")

# %% Inizializzazione interfaccia xml

aiuti_di_stato = AiutiDiStato()

# %% Creo file parser

test_file_name = r"data/AiutiDiStato/OpenData_Aiuti_2019_07.xml"

parser = XMLParser(test_file_name, aiuti_di_stato)

# %% Parse

df = parser.parse_xml()

# %%

df.info()

# %%
