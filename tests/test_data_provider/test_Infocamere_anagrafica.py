import unittest
from data_provider import AnagraficaInfocamere, DataProvider
from file_parser import ParserXls
import pandas as pd
import numpy as np

class Test_AnagraficaInfocamere(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.dp = AnagraficaInfocamere()

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    # Da cambiare ogni aggiornamento del Data Provider ------------------------
    def test_matching_columns_names(self):
        columns = [
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
        self.assertEqual(columns, self.dp.get_column_names())

    def test_first_row_matching(self):
        data = [
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
            ,pd.NaT
            ,pd.Timestamp('1969-01-30 00:00:00')
            ,pd.NaT
            ,pd.NaT
            ,np.nan
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
        self.assertEqual(data,
            self.dp.df.iloc[0,:].tolist())
    # -------------------------------------------------------------------------
    def test_class_inheritance_from_data_provider(self):
        self.assertTrue(issubclass(type(self.dp), DataProvider))

    def test_attributes_isinstance_df(self):
        self.assertTrue(isinstance(self.dp.df, pd.DataFrame))

    def test_attributes_isinstance_file_parser(self):
        self.assertTrue(isinstance(self.dp.file_parser, ParserXls))
    
    def test_attributes_isinstance_file_path(self):
        self.assertTrue(isinstance(self.dp.file_path, str))

    def test_attributes_isinstance_column_types(self):
        self.assertTrue(isinstance(self.dp.column_types, dict))

    def test_attributes_file_path(self):
        file_path = r"data/Infocamere/"
        self.assertEqual(file_path, self.dp.file_path)

    def test_attributes_column_types(self):
        column_types = {
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
            18: "object",        
            19: "object",        
            20: "object",        
            21: "object",        
            22: "object",        
            23: "object",        
            24: "object",        
            25: "object",        
            26: "object",        
            27: "object",        
            28: "object",        
            29: "object",        
            30: "object",        
            31: "object",        
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
        self.assertEqual(column_types, self.dp.column_types)