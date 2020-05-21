"""

11/05: Script realizzato per controllare il file sui finanziamenti UE per
lo script di matching di Ilaria

RISULTATO: Emergono aziende che non hanno vatNumber ma che
            nello script non riesco a filtrare (?)

21/05: inserito anche controllo su nuovi temi e schemi -> estrazione per 
        collega che deve fornirci le informazioni
"""
# %% Setup
import pandas as pd
import numpy as np

from file_parser import ParserCsv

FILE_PATH = r"../data/FinanziamentiUE/input/cordis-h2020organizations.csv"

# %% Open file
file_parser = ParserCsv(FILE_PATH)
file_data = file_parser.open_file(sep=';')

# %% Inspection the file with info()
file_data.info()

# %% Country inspection
file_data["country"].value_counts().head()

# %% Filter IT 
it_filter = file_data["country"] == "IT"
it_organizations = file_data.loc[it_filter]

# %% IT organizations inspection
it_organizations.info()

# %% VAT duplicates inspection
it_organizations["vatNumber"].describe(include='all')

# %% Subset organizations with and without VAT number
vat_notna_filter = it_organizations["vatNumber"].notna()
it_org_vat_ok = it_organizations.loc[vat_notna_filter]
it_org_vat_missing = it_organizations.loc[~ vat_notna_filter]

# %% Check who has vat number missing that is in it_org_vat_ok
id_for_missing_list = it_org_vat_missing["id"].tolist()
missing_with_vat_filter = it_org_vat_ok["id"] \
                                .isin(id_for_missing_list)

missing_with_vat_id_list = it_org_vat_ok.loc[missing_with_vat_filter]

# %% Update the missing organization DataFrame
id_missing_with_vat_filter = it_organizations["id"] \
                                    .isin(id_for_missing_list)

it_org_vat_missing = it_organizations.loc[ \
                            (~ vat_notna_filter) & \
                            id_missing_with_vat_filter ]

# %% Export organizations with missing vat
it_org_vat_missing.to_csv(
            r"../data/FinanziamentiUE/output/missingVat.csv",
            sep=";")

# %% Read output from script
OUTPUT_PATH = r"../data/FinanziamentiUE/output/eu_imprese_fvg_match_0520.csv"
output_parser = ParserCsv(OUTPUT_PATH)
output_df = output_parser.open_file(sep=';')

# %% Export into excel file
output_df.to_excel(r"../data/FinanziamentiUE/output/outputScript.xlsx")