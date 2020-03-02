"""
28/10/2019
Certificazione US 1725: Modifica calcolo dimensioni dell'azienda.
Sono ora tenuti in considerazione solo i numeri dei dipendenti recenti,
nello specifico degli ultimi 3 anni (compreso il valore max).
rispetto all'anno dell'ultima rilevazione dipendenti dell'anagrafica.
Per le imprese prive di questo dato si stima la dimensione in base ai 
dati di bilancio, se disponibili.
La stima in base ai dati di bilancio avviene quando l'ultimo bilancio
disponibile non è antecedente di 3 anni rispetto all'ultimo bilancio
presente nel DB.

Certificazione US 1724: Nuovo calcolo del valore aggiunto/addetto.

Innovation Intelligence in Python
Marco Matteo Buzzulini
"""
from innovation_intelligence.db_interface.anagrafica import Anagrafica
from innovation_intelligence.db_interface.bilanci import Bilanci

import pandas as pd
import numpy as np
import os
import datetime

def Controllo_dimensioneAziendale(anag, bil):
    # Prendo ultimo anno a disposizione dall'anagrafica
    last_year = anag.df['AnnoRilevazioneDipendenti'].value_counts() \
        .index.astype('int64').max()
    # Seleziono solo le imprese con DimensioneAziendale calcolata
    df_anag = anag.df.loc[ \
        (anag.df["DimensioneAziendale"] != "0. No data") & \
        ( ~ anag.df["DimensioneAziendale"].isna()) ]
    # Anni di riferimento
    years = [ i for i in range(last_year-2, last_year+1) ]
    # Distinguo quelle calcolate direttamente, che vanno bene
    cond = df_anag["AnnoRilevazioneDipendenti"].isin(years) 
    # df_anag_direttamente = df_anag.loc[cond]
    # Da quelle che devono essere controllate con i bilanci
    df_anag_indirettamente = df_anag.loc[ ~ cond ]
    cf_da_controllare = df_anag_indirettamente["CF"].to_numpy().tolist()
    # Imprese con una data rilevazione non nei 3 anni di riferimento
    df_bil = bil.df.loc[ \
        bil.df["CF"].isin(cf_da_controllare)]
    # Series con gli ultimi bilanci per CF
    idx_anno_max = df_bil.groupby('CF')['Anno'].idxmax()
    # Seleziono gli ultimi bilanci per CF
    df_bil_max = df_bil.loc[idx_anno_max]
    last_year_bil = bil.df['Anno'].value_counts() \
        .index.astype('int64').max()
    return df_bil_max.loc[ ~ df_bil_max['Anno'].isin(
        [i for i in range(last_year_bil-2, last_year_bil+1)]) ].empty

def Controllo_valAggSuAddetto(anag, bil):
    bil.df = bil.df.loc[ ~ bil.df["ValoreAggiuntoPerAddetto"].isna() ]
    cf_list = bil.df["CF"].drop_duplicates().to_numpy().tolist()
    anag.df = anag.df.loc[anag.df["CF"].isin(cf_list)]
    return Controllo_dimensioneAziendale(anag, bil)

def main():
    anag = Anagrafica()
    bil = Bilanci()
    test = Controllo_valAggSuAddetto(anag, bil)
    print(test)

if __name__ == '__main__':
    main()
