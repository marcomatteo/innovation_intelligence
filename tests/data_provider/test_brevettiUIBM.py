from tests import TestDataProviderBaseClass
from file_parser import ParserXls
from data_provider import BrevettiIta

import pandas as pd
import numpy as np


class Test_BrevettiIta(TestDataProviderBaseClass):

    @classmethod
    def setUpClass(cls):
        cls.dp = BrevettiIta(inTest=True)
        cls.file_parser = ParserXls
        cls.file_path = r"data/data_tests/UIBM/"
        cls.columns = [
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
        cls.first_row = [
            10005475,
            '102015000005436',
            pd.Timestamp('2015-02-04 00:00:00'),
            'Aisico S.r.l.',
            np.nan,
            '10186871009',
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            'SISTEMA DI MISURA AD ALTO RENDIMENTO DELLA VISIBILITÀ NOTTURNA DELLA SEGNALETICA STRADALE VERTICALE.',
            'G',
            '06',
            'K',
            0
        ]
        cls.column_types = {
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
        cls.column_constraints = {
            i: False for i in range(16)
        }
