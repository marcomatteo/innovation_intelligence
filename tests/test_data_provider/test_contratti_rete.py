import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np

from tests import TestDataProviderBaseClass
from file_parser import ParserXls

import data_provider

class Test_ContrattiRete(TestDataProviderBaseClass):
    
    @classmethod
    def setUpClass(cls):
        cls.dp = data_provider.ContrattiRete(inTest=True)
        cls.file_parser = ParserXls
        cls.file_path = r"data/data_tests/ContrattiRete/"

        cls.columns = [ "progr."
            ,"denominazione contratto"
            ,"data atto"
            ,"numero repertorio"
            ,"numero atto"
            ,"oggetto"
            ,"n.rea"
            ,"c.f."
            ,"denominazione impresa"
            ,"impresa di riferimento"
            ,"comune"
            ,"REG"
            ,"PV"
            ,"NG"
            ,"codice ATECO 2007"
            ,"settore attivita'"
            ,"sezione attivita'"
            ,"attivita'"
            ,"SoggettoGiuridico"
        ]

        cls.first_row = [ 3
            ,"MECNET"
            ,"10/09/2010"
            ,"199466/46658"
            , np.nan
            ,"Svolgimento nellambito della rete delle attività che le singole imprese non sono in grado di gestire al proprio interno, attività comuni finalizzate allaumento della qualità dei prodotti e alla loro certificazione, par"
            , 151153
            ,"00963010301"
            ,"B  T OFFICINE MECCANICHE S.R.L."
            , np.nan
            ,"POVOLETTO"
            , 6
            ,"UD"
            ,"SR"
            , "2562"
            ,"INDUSTRIA/ARTIGIANATO"
            ,"C ATTIVITA' MANIFATTURIERE"
            ,"C 25 FABBRICAZIONE DI PRODOTTI IN METALLO (ESCLUSI MACCHINARI E A"
            ,"NO"
        ]
        
        cls.column_types = {
            0: 'int',
            1: 'object',
            2: 'date',
            3: 'object',
            4: 'object',
            5: 'object',
            6: 'object',
            7: 'object',
            8: 'object',
            9: 'object',
            10: 'object',
            11: 'object',
            12: 'object',
            13: 'object',
            14: 'object',
            15: 'object',
            16: 'object',
            17: 'object',
            18: 'object'
        }
        
        cls.column_constraints = {i: False for i in range(len(cls.columns))}
        cls.column_constraints[3] = True    # numero repertorio
        cls.column_constraints[4] = True    # numero atto
        cls.column_constraints[7] = True    # c.f.
