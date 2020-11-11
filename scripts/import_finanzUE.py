"""
Script per controllo importazione dei Finanziamenti UE data 08/05/2020
"""
# %% Setup
import pandas as pd
from file_parser import ParserXls
from idb import DatabaseConnector
import os
os.chdir("..")

# %% Parameters
BASE_DIR = r"data/FinanziamentiUE/2020/"
FILE_NAME = "FinanziamentiUE_08_05_2020.xlsx"
ORGANIZATION_SHEET = "organizations"
PROJECTS_SHEET = "projects"
ORGANIZATION_TBL_NAME = "DATA_FinanziamentiUE_Impresa"
PROJECTS_TBL_NAME = "DATA_FinanziamentiUE_Progetto"

# %% Loading
finanziamentiUE_parser = ParserXls(BASE_DIR + FILE_NAME)
finanziamentiUE_parser.sheet_names

# %% Open organizations
finanziamentiUE_organizations_df = finanziamentiUE_parser.open_file(
    ORGANIZATION_SHEET)
finanziamentiUE_organizations_df.info()

# %% Open projects
finanziamentiUE_projects_df = finanziamentiUE_parser.open_file(PROJECTS_SHEET)
finanziamentiUE_projects_df.info()

# %% Open DB connection
db = DatabaseConnector()

# %% Open Organizazions tbl
tbl_organizations = db.get_dataframe_from_table(ORGANIZATION_TBL_NAME)

# %% Open Projects tbl
tbl_projects = db.get_dataframe_from_table(PROJECTS_TBL_NAME)

# %%[markdown]
# Check se tutte le imprese sono state importate

# %% Cleaning vatNumber column


def clean_vat_number(word):
    return str(word)[2:]


finanziamentiUE_organizations_df["CF"] = finanziamentiUE_organizations_df["vatNumber"].map(
    lambda word: clean_vat_number(word))

# %% Getting only valid CFs


def get_valid_CF_list(column: pd.Series) -> list:
    valid_start_number = list(map(lambda number: str(number), range(10)))
    cf_all = column.drop_duplicates().tolist()

    return list(filter(lambda word: word[0] in valid_start_number, cf_all))


cf_list = get_valid_CF_list(finanziamentiUE_organizations_df["CF"])


# %% Getting DB
tbl_cf = db.get_dataframe_from_query("SELECT DISTINCT CF FROM DATA_Impresa")

# %% Merge

df = finanziamentiUE_organizations_df.merge(
    tbl_cf, how="left", on="CF", indicator=True)

# %% Only in DB

filter_cf = df["_merge"] == 'both'
df_to_check = df.loc[filter_cf]

# %% File output per controllo a campione

df_to_check.to_excel("FinanziamentiDaControllare.xlsx")

# %% da implementare

# # %% Cast delle colonne per il merge
# projects_df = projects_df.astype({"id": 'int64'})
# org_df = org_df.astype({'projectID': 'int64'})

# # %% Effettuo il merge tra il dataset dei progetti e quello delle organizations
# finUE_df = projects_df.merge(
#     org_df,
#     left_on="id", right_on="projectID",
#     how="inner",
#     suffixes=("_projects", "_organizations")
# )
