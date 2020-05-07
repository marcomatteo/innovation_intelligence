import unittest
from data_provider import BilanciInfocamere, DataProvider
from file_parser import ParserXls
import pandas as pd
import numpy as np

class Test_BilanciInfocamere(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.dp = BilanciInfocamere()

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    # Da cambiare ogni aggiornamento del Data Provider ------------------------
    def test_matching_columns_names(self):
        columns = [
            "c fiscale",                
            "cia",                                             
            "rea",                                             
            "anno",                                            
            "Totale attivo",                                   
            "Totale Immobilizzazioni immateriali",             
            "Crediti esigibili entro l'esercizio successivo",  
            "Totale patrimonio netto",                         
            "Debiti esigibili entro l'esercizio successivo",   
            "Totale valore della produzione",                  
            "Ricavi delle vendite",                            
            "Totale Costi del Personale",                      
            "Differenza tra valore e costi della produzione",  
            "Ammortamento Immobilizzazione Immateriali",       
            "Utile/perdita esercizio ultimi",                  
            "valore aggiunto",                                 
            "tot.aam.acc.svalutazioni",                        
            "(ron) reddito operativo netto"            
        ]
        self.assertEqual(columns, self.dp.get_column_names())

    def test_first_row_matching(self):
        data = [
            "00002070324",
            "TS",
            65026,
            2017,
            2029166,
            8741,
            951876,
            541838,
            1244812,
            2131563,
            2114316,
            622338,
            539200,
            3180,
            521523,
            1176227,
            14689,
            539200
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
            10: "object",
            11: "object",
            12: "object",
            13: "object",
            14: "object",
            15: "object",
            16: "object",
            17: "object",
        }
        self.assertEqual(column_types, self.dp.column_types)