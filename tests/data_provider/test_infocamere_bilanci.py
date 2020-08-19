from tests import TestDataProviderBaseClass
from data_provider import BilanciInfocamere
from file_parser import ParserXls

import unittest
import pandas as pd
import numpy as np

class Test_BilanciInfocamere(TestDataProviderBaseClass):
    
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.dp = BilanciInfocamere(inTest=True)
        cls.file_path = r"data/data_tests/Infocamere/"
        cls.file_parser = ParserXls
        
        cls.columns = [
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
        
        cls.first_row = [
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
        
        cls.column_types = {
            0: 'object',
            1: 'object',
            2: 'object',
            3: 'int',
            4: 'float',
            5: 'float',
            6: 'float',
            7: 'float',
            8: 'float',
            9: 'float',
            10: 'float',
            11: 'float',
            12: 'float',
            13: 'float',
            14: 'float',
            15: 'float'
        }
        cls.column_constraints = {i: False for i in range(16)}
        cls.column_constraints[0] = True    # c.f.
        cls.column_constraints[1] = True    # pv
        cls.column_constraints[3] = True    # sede/ul