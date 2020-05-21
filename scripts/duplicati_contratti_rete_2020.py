"""

Script per controllare il file fonte dei Contratti di Rete

Questo script è stato creato per poi consolidare il data provider

"""
# %% Setup
from file_parser import ParserXls
import pandas as pd
import numpy as np

FILE_PATH = r"../data/ContrattiRete/ContrattiRete_3Apr2020.xlsx"

# %% Apro il file utilizzando abbrv. 'contratti' per i Contratti di rete
try:
    contratti_parser = ParserXls(FILE_PATH)
except Exception as e:
    print("Problemi con il percorso del file")
    raise e
 
# %% Leggo il file
contratti_df = contratti_parser.open_file(sheet_name='Elenco')
contratti_df.info()

# %% Conteggio duplicati
column_name_constraints = ['numero repertorio', 'numero atto', 'c.f.']

contratti_duplicates_filter = contratti_df \
                                .duplicated(subset = column_name_constraints,
                                            keep = False)
contratti_duplicates_df = contratti_df.loc[contratti_duplicates_filter]
# %% Verifica dei CF duplicati
def get_valid_contratti(df: pd.DataFrame) -> pd.DataFrame:

    def isValidFiscalCode(cf : str) -> bool:
        cf_trimmed = cf.strip()
        if len(cf_trimmed) > 11:
            return False
        elif len(cf_trimmed) == 0:
            return False
        elif cf_trimmed == "":
            return False
        else:
            return True

    df["check_col"] = df["c.f."].map(
                        lambda value: isValidFiscalCode(str(value))) 
    check_col_filter = df["check_col"]

    return df.loc[check_col_filter]

contratti_valid_duplicates_df = get_valid_contratti(contratti_duplicates_df)

# %% contratti_valid_duplicates_df inspection
contratti_valid_duplicates_df.info()

# %% Riordino per visualizzazione
contratti_valid_duplicates_df["data atto"] = pd.to_datetime(
                                    contratti_valid_duplicates_df["data atto"])
contratti_valid_duplicates_df.sort_values(
                                by = ["data atto", "c.f."], inplace = True)

# %% Stampo risultato su excel per il kickoff
contratti_valid_duplicates_df.to_excel(
            r"../data/ContrattiRete/ContrattiRete_3Apr2020_duplicati.xlsx")