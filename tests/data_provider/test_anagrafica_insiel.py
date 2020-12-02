from pandas._libs.tslibs import NaT
from tests import TestDataProviderBaseClass
from data_provider import AnagraficaInsiel
from file_parser import ParserXls

import pandas as pd
import numpy as np

class Test_AnagraficaInsiel(TestDataProviderBaseClass):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.dp = AnagraficaInsiel(inTest=True)
        cls.file_parser = ParserXls
        cls.file_path = r"data/data_tests/Insiel/"

        cls.columns = [
            "c fiscale",
            "PRV - Provincia"                                                 ,
            "N-REG-IMP - Numero Registro Imprese"                             ,
            "rea"                                                             ,
            "UL-SEDE - Unità Locale o sede dell'impresa"                      ,
            "N-ALBO-AA - Numero di iscrizione all'Albo Imprese Artigiane"     ,
            "SEZ-REG-IMP - Sezione di iscrizione dell'impresa al Registro del",
            "NG - Natura Giuridica"                                           ,
            "natura giuridica"                                                ,
            "tipo impresa"                                                    ,
            "DT-ISCR-RI - Data di iscrizione al Registro Imprese"             ,
            "DT-ISCR-RD - Data di iscrizione al Registro delle Ditte"         ,
            "DT-ISCR-AA - Data di iscrizione all'Albo delle Imprese Artigiane",
            "DT-APER-UL - Data di apertura dell'Unità Locale"                 ,
            "cancellazione"                                                   ,
            "DT-INI-AT - Data di inizio attività dell'impresa"                ,
            "dt cessazione attività"                                          ,
            "fallimento"                                                      ,
            "DT-LIQUID - Data liquidazione dell'impresa"                      ,
            "DENOMINAZIONE - Denominazione dell'impresa"                      ,
            "INDIRIZZO"                                                       ,
            "STRAD - Via"                                                     ,
            "CAP"                                                             ,
            "COMUNE"                                                          ,
            "FRAZIONE"                                                        ,
            "ALTRE-INDICAZIONI - Altre indicazioni relative all'indirizz del" ,
            "AA-ADD - Anno di dichiarazione degli addetti"                    ,
            "IND - Numero addetti indipendenti"                               ,
            "DIP - Numero addetti dipendenti"                                 ,
            "PARTITA IVA"                                                     ,
            "TELEFONO"                                                        ,
            "CAPITALE - Capitale sociale dell'impresa"                        ,
            "ATTIVITA' - Descrizione dell'attività principale dell'impresa"   ,
            "VALUTA-CAPITALE - Valuta del capitale sociale dell'impresa"      ,
            "stato impresa/ul"                                                ,
            "tipo sede/ul1"                                                   ,
            "tipo sede/ul2"                                                   ,
            "tipo sede/ul3"                                                   ,
            "tipo sede/ul4"                                                   ,
            "tipo sede/ul5"                                                   ,
            "Presenza di sedi secondarie all'estero"                          ,
            "Impresa estera con unità locale in Friuli Venezia Giulia"        ,
            "sezione Impresa - Indicazione delle imprese che sono PMI"        ,
            "sezione Impresa - Indicazione delle imprese che sono start up"   ,
            "Impr Femminile"                                                  ,
            "Impr Giovane"                                                    ,
            "Impr Straniera"                                                  ,
            "pec"                                                             ,
            "Cessazione artigiana"                                            ,                                              
            "DT-COST - Data costituzione"                                     ,
            "Tipo Localizzazione"
            ]
        
        cls.first_row = [
            "00000470310"
            ,"GO"
            ,"(GO007-1352)"
            ,37843
            ,"SEDE"
            ,np.nan
            ,"O"
            ,"SN"
            ,"SN - SOCIETA' IN NOME COLLETTIVO"
            ,"Società"
            ,pd.Timestamp('1996-02-19 00:00:00')
            ,pd.Timestamp('1975-01-14 00:00:00')
            ,pd.NaT
            ,pd.NaT
            ,np.nan
            ,pd.NaT
            ,pd.NaT
            ,pd.NaT
            ,pd.NaT
            ,"PELLIZZARI SILVIO DI SEVERINO PELLIZZARI E C. S.N.C."
            ,"VIA PESCHERIA 4"
            ,np.nan
            ,'34071'
            ,"CORMONS - GO"
            ,np.nan
            ,np.nan
            ,1999
            ,0
            ,0
            ,"00000470310"
            ,"0481/60323"
            ,np.nan
            ,'COMMERCIO AL MINUTO TAB. MERC. I - II (SOLTANTO CARNE PRECONFEZIONATA); VI\n(SOLTANTO PRODOTTI PRECONFEZIONATI) E XIV (ESCLUSIVAMENTE PER LE SEGUENTI VOCI:\n"GASTRONOMIA" "PROFUMERIA", CARTOLERIA, CANCELLERIA E ARTICOLI SCOLASTICI,\nLIBRERIA, MATERIE PLA ...'
            ,np.nan
            ,"INATTIVA"
            ,np.nan
            ,np.nan
            ,np.nan
            ,np.nan
            ,np.nan
            ,np.nan
            ,np.nan
            ,"NO"
            ,"NO"
            ,"NO"
            ,"NO"
            ,"NO"
            ,"PELLIZZARI@PEC.CGN.IT"
            ,pd.NaT
            ,pd.Timestamp('1974-08-26 00:00:00')
            ,"SE - SEDE PRINCIPALE"
            ]

