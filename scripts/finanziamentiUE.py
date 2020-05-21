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

from file_parser import ParserCsv, ParserXls
from idb import DatabaseConnector

# %% [markdown]
# Procedura per preparare il file dei finanziamenti UE al matching
# e in seguito alla creazione del file finale da caricare in I2FVG

# %% Leggo il file csv scaricato delle organizations
FILE_PATH = r"../data/FinanziamentiUE/input/cordis-h2020organizations.csv"
file_parser = ParserCsv(FILE_PATH)
file_data = file_parser.open_file(sep=';')

# %% Inspection the file with info()
file_data.info()

# %% Country inspection
file_data["country"].value_counts().head()

# %% Filtro solo le imprese / organizzazioni italiane
it_filter = file_data["country"] == "IT"
it_organizations = file_data.loc[it_filter]

# %% IT organizations inspection
it_organizations.info()

# %% VAT duplicates inspection
it_organizations["vatNumber"].describe(include='all')

# %% Separo le organizations che hanno un codice fiscale associato
# Da quelle che non hanno un codice fiscale
vat_notna_filter = it_organizations["vatNumber"].notna()

it_org_vat_ok = it_organizations.loc[vat_notna_filter]
it_org_vat_missing = it_organizations.loc[~ vat_notna_filter]

# %% Per scrupolo controllo che: coloro che non hanno un codice fiscale
# non sia presente nel dataframe di imprese che hanno un codice fiscale
# effettuando un check sugli id
id_for_missing_list = it_org_vat_missing["id"].tolist()

missing_with_vat_filter = it_org_vat_ok["id"] \
    .isin(id_for_missing_list)

missing_with_vat_id_list = it_org_vat_ok.loc[missing_with_vat_filter]
missing_with_vat_id_list.info()

# %% Update the missing organization DataFrame
id_missing_but_with_vat_list = missing_with_vat_id_list["id"] \
    .drop_duplicates().tolist()

id_missing_but_with_vat_filter = it_organizations["id"] \
    .isin(id_missing_but_with_vat_list)

# Estraggo coloro che non hanno un codice fiscale e quelli che
# non hanno un codice fiscale ma hanno un id uguale a quelli
# che hanno un codice fiscale
it_org_vat_missing = it_organizations.loc[
    (~ vat_notna_filter) &
    (~ id_missing_but_with_vat_filter)]

# %% Esporto il csv per effettuare il matching con script
it_org_vat_missing.to_csv(
    r"../data/FinanziamentiUE/output/missingVat.csv",
    sep=";")

# %% [markdown]
# Dopo aver eseguito lo script di Ilaria, apro il file del matching
# e lo salvo in excel

# %% Read matching from script
OUTPUT_PATH = r"../data/FinanziamentiUE/output/eu_imprese_fvg_match_0520.csv"
output_parser = ParserCsv(OUTPUT_PATH)
output_df = output_parser.open_file(sep=';')

# %% Esporto in excel il file per il controllo manuale
output_df.to_excel(r"../data/FinanziamentiUE/output/outputScript.xlsx")

# %% Leggo il file dello script controllato manualmente
MATCHING_PATH = r"../data/FinanziamentiUE/output/risultato_matching.xlsx"
matching_df = ParserXls(MATCHING_PATH).open_file()

# %% Inserisco colonna
matching_df["vatNumber_match"] = matching_df['anag_cf'].map(
    lambda cf: "IT" + str(cf))

# %% Faccio il merge con it_organizations
it_organizations = it_organizations.merge(
    matching_df[["eu_id", "vatNumber_match"]], left_on="id", right_on="eu_id",
    how="left")
it_organizations.info()

# %% Applico il filtro per le imprese con match
matched_organizations_filter = it_organizations["vatNumber_match"].notna()

it_organizations.loc[matched_organizations_filter,
                     "vatNumber"] = it_organizations.loc[matched_organizations_filter,
                                                         "vatNumber_match"]

# %% Rimuovo colonne non più necessarie
it_organizations.drop(columns=['eu_id', "vatNumber_match"], inplace=True)


# %% Salvo il file in un excel
it_organizations.to_excel(
    r"../data/FinanziamentiUE/org_matched_it.xlsx", index=False)

# %% [markdown]
# Lavoro di estrazione nuovi Temi e Schemi di finanziamento UE

# %% Leggo il file csv scaricato dei projects
PROJ_PATH = r"../data/FinanziamentiUE/input/cordis-h2020projects.csv"
proj_parser = ParserCsv(PROJ_PATH)
proj_data = proj_parser.open_file(sep=';')

# %% Esamino il file dei progetti
proj_data.info()

# %% Effettuo il merge tra il dataset dei progetti e quello delle organizations
projects_df = proj_data.merge(
    it_organizations,
    left_on="id", right_on="projectID",
    how="inner",
    suffixes=("_projects", "_organizations")
)

projects_df.info()

# %% Ottengo i codici fiscali dal Database e li salvo in una lista
CF_QUERY = "SELECT DISTINCT CF FROM DATA_Impresa"
cf_from_db = DatabaseConnector().get_dataframe_from_query(CF_QUERY)

cf_list = cf_from_db["CF"].tolist()

# %% Pulizia campo vatNumber
projects_df.loc[:, "vatNumber"] = projects_df["vatNumber"].map(
    lambda cf: str(cf)[2:])

# %% Filtro le imprese presenti nel DB
cf_from_db_filter = projects_df["vatNumber"].isin(cf_list)

projects_i2fvg_df = projects_df.loc[cf_from_db_filter]
projects_i2fvg_df.info()

# %% Ottengo topics e fundingScheme
topics = projects_i2fvg_df["topics"].drop_duplicates()
fundingScheme = projects_i2fvg_df["fundingScheme"].drop_duplicates()

# %% Pulizia di campi non previsti


def cleaning_series(series: pd.Series) -> pd.Series:
    series = series.map(lambda x: x.replace("\\", ""))
    series = series.map(lambda x: x.replace("/", ""))
    series = series.map(lambda x: x.lstrip())
    return series


topics = cleaning_series(topics)
fundingScheme = cleaning_series(fundingScheme)

# %% Apro file temi scaricati
TOPICS_I2FVG_FILE = r"../data/FinanziamentiUE/input/topics.xlsx"

topics_i2fvg_df = ParserXls(TOPICS_I2FVG_FILE).open_file()
topics_i2fvg_df.info()

# %% Creo liste per effettuare il filtro
topics_i2fvg_list = topics_i2fvg_df.iloc[:, 1].drop_duplicates().tolist()

topics_filter = topics.isin(topics_i2fvg_list)
topics_missing = topics.loc[~topics_filter]

topics_missing.describe()

# %% Apro file schemi scaricati
FUNDING_I2FVG_FILE = r"../data/FinanziamentiUE/input/fundingScheme.xlsx"

fundingScheme_i2fvg_df = ParserXls(FUNDING_I2FVG_FILE).open_file()
fundingScheme_i2fvg_df.info()

# %% Creo liste ed effettuo il filtro
fundingScheme_i2fvg_list = fundingScheme_i2fvg_df.iloc[:, 1].drop_duplicates(
).tolist()

funding_filter = fundingScheme.isin(fundingScheme_i2fvg_list)
fundingScheme_missing = fundingScheme.loc[~funding_filter]

fundingScheme_missing.describe()

# %% Salvo i risultati dell'ispezione nella cartella output
topics_missing.to_frame().to_excel(r"../data/FinanziamentiUE/output/topics_mancanti.xlsx",
                                   index=False)

fundingScheme_missing.to_frame().to_excel(r"../data/FinanziamentiUE/output/fundingScheme_mancanti.xlsx",
                                          index=False)


# %%
