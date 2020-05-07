from tests import TestDataProviderBaseClass
from file_parser import ParserXls
from data_provider import BrevettiIta

import pandas as pd
import numpy as np

class Test_BrevettiIta(TestDataProviderBaseClass):
    
    @classmethod
    def setUpClass(cls):
        cls.dp = BrevettiIta()

    def test_matching_columns_names(self):
        self.columns = [
            'ID_APPLICATION',
            'NUMERO_DOMANDA',
            'DATA_DEPOSITO',
            'COGNOME_DENOMINAZIONE',
            'NOME',
            'CF_PARTITA_IVA',
            'INDIRIZZO',
            'NUMERO_CIVICO',
            'CITTÀ',
            'PROVINCIA',
            'TITOLO',
            'SEZIONE',
            'CLASSE',
            'SOTTOCLASSE',
            'UNDER_WRAPS'
        ]
        super().test_matching_columns_names()

    def test_first_row_matching(self):
        self.first_row = [
            10479772,
            '102018000000176',
            pd.Timestamp('2018-01-02 00:00:00'),
            'EVERY WAVE S.R.L.',
            np.nan,
            '05064670283',
            'Via Martiri delle Foibe',
            '2/1',
            'Vigonza',
            'Padova',
            'DISPOSITIVO DI PULIZIA E SBLOCCO DI STRUTTURE MECCANICHE',
            'B',
            '29',
            'D',
            0
        ]
        super().test_first_row_matching()

    def test_attributes_file_path(self):
        self.file_path = r"data/UIBM/"
        super().test_attributes_file_path()

    def test_attributes_column_types(self):
        self.column_types = {
            0: 'int',
            1: 'object',
            2: 'date',
            3: 'object',
            4: 'object',
            5: 'int',
            6: 'object',
            7: 'object',
            8: 'object',
            9: 'object',
            10: 'object',
            11: 'object',
            12: 'object',
            13: 'object',
            14: 'object',
            15: 'bool'
        }
        super().test_attributes_column_types()

    def test_attributes_column_constraints(self):
        self.column_constraints = {
            i: False for i in range(16)
        }
        super().test_attributes_column_constraints()

    def test_class_inheritance_from_data_provider(self):
        super().test_class_inheritance_from_data_provider()
    
    def test_attributes_isinstance_df(self):
        super().test_attributes_isinstance_df()

    def test_attributes_isinstance_file_parser(self):
        self.file_parser = ParserXls
        super().test_attributes_isinstance_file_parser()