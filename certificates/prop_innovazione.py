"""
23/10/2019
Certificazione US 1726: Modifica calcolo propensione innovazione.
Sono ora tenuti in considerazione solo i brevetti vecchi massimo 10 anni
rispetto all'anno dell'ultimo brevetto importato sulla piattaforma.

Propensione innovazione:
- presenza di un brevetto
- presenza di un finzanziamento fvg e/o europeo
- start up innovative
- pmi innovativa

Innovation Intelligence in Python
Marco Matteo Buzzulini
"""
#TODO: per certificare il BUG 2283
from innovation_intelligence.db_interface.brevetti import Brevetti
from innovation_intelligence.db_interface.finanziamenti import Finanziamenti
from db_interface import Anagrafica

import pandas as pd
import numpy as np
import os
import datetime

def Controllo_PropensioneInnovazione():
    """
    Controlla sul DB di Innovation Intelligence se l'indicatore di propensione
    all'innovazione dell'anagrafica (PropensioneRicercaSviluppoLivello) è 
    calcolato correttamente.
    
    Ritorna: Check (True/False), pandas.DataFrame
    """
    print("Apertura delle tabelle di Innovation Intelligence...")
    anag = Anagrafica()
    finanz = Finanziamenti()
    brevetti = Brevetti()

    print("Effettuo la selezione dei criteri...")
    # Seleziono solo le imprese con propensione all'innovazione oggettiva
    tbl_imprese = anag.tbl_df['sedi'].set_index('CF')
            
    # Conto i brevetti per azienda in una pd.Series
    # Prendo in considerazione come anno di rif quello dell'ultimo brevetto
    anno_brevetto_max = pd.Timestamp(brevetti.df['DataDeposito'].max())
    # Sottraggo 10 anni come vuole il nuovo periodo di riferimento
    anno_brevetto_min = pd.Timestamp(
        datetime.date(anno_brevetto_max.year - 10, 1, 1))

    cond_type = (brevetti.df['RF_Brevetti_TipoBrevetto'] == 1) | \
                (brevetti.df['RF_Brevetti_TipoBrevetto'] == 2) | \
                (brevetti.df['RF_Brevetti_TipoBrevetto'] == 3) 
    cond_date = (brevetti.df['DataDeposito'] >= anno_brevetto_min) & \
                (brevetti.df['DataDeposito'] <= anno_brevetto_max)

    tbl_brevetti = brevetti.df.loc[ cond_type & cond_date] \
            .groupby('CF')['Titolo'].count().rename("Brevetti")

    # Conto i finanziamenti per azienda in una pd.Series
    cond_finanziamenti = finanz.df['TipoProgramma'].notna()
    tbl_finanz = finanz.df.loc[cond_finanziamenti] \
            .groupby('CF')['Finanziamento'] \
            .sum().rename("Finanziamenti")
    
    # Unisco tutte i df alle imprese oggettivamente innovative 
    tbl_check = tbl_imprese.join(
        # I brevetti per CF
        tbl_brevetti.to_frame().join(
            # I finanziamenti per CF
            tbl_finanz,
            how = 'outer',
            lsuffix = '_brevetti',
            rsuffix = '_finanziamenti'
        ),
        how = "left",
        lsuffix = '_impresa',
        rsuffix = '_brevetti'
    ).loc[:,[
        "Denominazione",
        "PropensioneRicercaSviluppoLivello",
        "Brevetti",
        "Finanziamenti",
        "StartUpFlag",
        "ImpresaInnovativaFlag"]]

    cond_brevetti = tbl_check['Brevetti'].notna()
    cond_fin = tbl_check['Finanziamenti'].notna()
    cond_startup = tbl_check['StartUpFlag'] == True
    cond_innovazione = tbl_check['ImpresaInnovativaFlag'] == True
    cond_oggettiva = tbl_check['PropensioneRicercaSviluppoLivello'] == 'Oggettiva'
    
    # Controllo sui falsi negativi
    check = (cond_brevetti | cond_fin | cond_startup | cond_innovazione) & cond_oggettiva
    if tbl_check.loc[check].empty:
        falseNeg = False
    else:
        falseNeg = True

    # Controllo sui falsi positivi
    check = ((~cond_brevetti) & (~cond_fin) & (~cond_startup) & (~cond_innovazione)) & cond_oggettiva
    if tbl_check.loc[check].empty:
        falsePos = False
    else:
        falsePos = True
    
    # Output
    if falsePos:
        print("\nSono presenti imprese oggettivamente innovative senza requisiti (presenza falsi positivi).")
    if falseNeg:
        print("\nSono presenti imprese non innovative ma che hanno i requisiti per esserlo (presenza falsi negativi).")

    return falseNeg, falsePos, tbl_check

if __name__ == '__main__':
    falseNeg, falsePos, df = Controllo_PropensioneInnovazione()
    if falsePos:
        print("\nSono presenti imprese oggettivamente innovative senza requisiti (presenza falsi positivi).")
    if falseNeg:
        print("\nSono presenti imprese non innovative ma che hanno i requisiti per esserlo (presenza falsi negativi).")