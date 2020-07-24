from tests import TestDataProviderBaseClass
from data_provider import AnagraficaInfocamere
from file_parser import ParserXls

import unittest
import pandas as pd
import numpy as np

class Test_AnagraficaInfocamere(TestDataProviderBaseClass):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.dp = AnagraficaInfocamere(inTest=True)
        cls.file_parser = ParserXls
        cls.file_path = r"data/data_tests/Infocamere/"

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
            "pec"                                                             
        ]
        
        cls.first_row = [
            "00002070324"
            ,"TS"
            ,"(TS006-7084)"
            ,65026
            ,"SEDE"
            ,np.nan
            ,"O"
            ,"SR"
            ,"SR - SOCIETA' A RESPONSABILITA' LIMITATA"
            ,"SOCIETA' DI CAPITALE"
            ,pd.Timestamp('1996-02-19 00:00:00')
            ,pd.Timestamp('1969-01-30 00:00:00')
            ,pd.NaT         # Non è np.nan perché la colonna è tipo data
            ,pd.NaT         # e non tipo 'object' come le altre
            ,np.nan
            ,pd.Timestamp('1969-01-30 00:00:00')
            ,np.nan
            ,pd.NaT
            ,pd.NaT
            ,"B.F.B. - CASA DI SPEDIZIONI S.R.L."
            ,"VIA CORTI 2"
            ,np.nan
            ,"34123"
            ,"TRIESTE - TS"
            ,np.nan
            ,np.nan
            ,2019
            ,0
            ,16
            ,"00002070324"
            ,"040/3220798"
            ,20000
            ,"SPEDIZIONI DOGANALI"
            ,"EURO"
            ,"ATTIVA"
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
            ,"claudio.brosch@pec.bfbtrieste.com"
        ]
        
        cls.column_types = {
            0: "object",        
            1: "object",
            2: "object",
            3: "object",
            4: "object",
            5: "object",
            6: "object",
            7: "object",
            8: "object",
            9: "object",
            10: "date",
            11: "date",
            12: "date",
            13: "date",
            14: "date",
            15: "date",
            16: "date",
            17: "date",
            18: "date",        
            19: "object",        
            20: "object",        
            21: "object",        
            22: "object",        
            23: "object",        
            24: "object",        
            25: "object",        
            26: "int",        
            27: "object",        
            28: "int",        
            29: "object",        
            30: "object",        
            31: "float",        
            32: "object",        
            33: "object",        
            34: "object",        
            35: "object",        
            36: "object",        
            37: "object",        
            38: "object",        
            39: "object",        
            40: "object",        
            41: "object",        
            42: "object",        
            43: "object",        
            44: "object",        
            45: "object",        
            46: "object",        
            47: "object",        
            48: "object",        
        }

        cls.column_constraints = {i: False for i in range(len(cls.columns))}
        cls.column_constraints[0] = True    # c.f.
        cls.column_constraints[1] = True    # provincia
        cls.column_constraints[4] = True    # sede/ul