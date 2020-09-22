# %% Setup
import os
import pandas as pd
os.chdir("..")
# %% Load DB connector
from idb import DatabaseConnector
db = DatabaseConnector()
# %% Query Bilanci
query = "SELECT CF, Anno, RicaviVendite FROM DATA_Bilancio" #+ " WHERE Anno > 2014"
bilanci = db.get_dataframe_from_query(query=query)
# %% Aziende DataFrame
query = "SELECT CF, ImpresaDinamicaFlag FROM DATA_Impresa"
aziende = db.get_dataframe_from_query(query=query)
aziende.set_index("CF", inplace=True)
# %% Raggruppamento
grouped = bilanci.groupby("CF")
# %% Ottengo i bilanci per azienda
def get_cf_years(df: pd.DataFrame):
    return df["Anno"].sort_values(ascending=True).values

years = grouped.apply(get_cf_years).rename("years")
# %% Lista imprese dinamiche
dinamica_filter = aziende.ImpresaDinamicaFlag == True
dinamiche_list = aziende.loc[dinamica_filter].index.tolist()
# %% Select to_check
year_df = years.to_frame().reset_index()
dinamiche_filter = year_df["CF"].isin(dinamiche_list)
to_check = year_df.loc[dinamiche_filter]
to_check.sample(n=10)
# %% Aggiungo l'info di quanti bilanci ci sono
to_check["num"] = to_check["years"].apply(lambda l: len(l))
to_check["num"].value_counts()
# %% Aggiungo informazione sui salti
def get_jumps(elem_list):
    jumps = []
    for i, el in enumerate(elem_list):
        if i > 0: # from second element
            diff = el - elem_list[i-1]
            if diff > 1:
                jumps.append(True)
            else:
                jumps.append(False)
    return jumps
            
def is_jump(elem_list):
    """Check where there is a jump in years"""
    if any(elem_list):
        return True
    return False

to_check["jumps"] = to_check["years"].map(lambda l: get_jumps(l))
to_check["isJump"] = to_check["jumps"].map(lambda l: is_jump(l))
# %% Controllo aziende con salti
jump_filter = to_check["isJump"] == True
to_validate_with_jumps = to_check.loc[jump_filter]
# %% Ottengo gli scenari
def get_scenario(elem_list):
    is2015 = 2015 in elem_list
    is2016 = 2016 in elem_list
    is2017 = 2017 in elem_list
    is2018 = 2018 in elem_list

    if is2015 and is2016 and is2017 and is2018:
        return "scenario1"
    elif (not is2015) and is2016 and is2017 and is2018:
        return "scenario2"
    elif is2015 and (not is2016) and is2017 and is2018:
        return "scenario3"
    elif is2015 and is2016 and (not is2017):
        return "scenario4"
    elif is2015 and is2016 and is2017 and (not is2018):
        return "scenario5"
    else:
        return "no_scenario"

to_check["scenari"] = to_check["years"].map(lambda l: get_scenario(l))
to_check["scenari"].value_counts()
# %%
to_check.to_excel("Analisi_dinamiche.xlsx")
# %%
aziende.ImpresaDinamicaFlag.value_counts()