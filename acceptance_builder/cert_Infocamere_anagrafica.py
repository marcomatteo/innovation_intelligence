from acceptance_builder import AcceptanceBuilder
from data_provider import AnagraficaInfocamere

import numpy as np
import logging

logger = logging.getLogger(__name__)


class AnagraficaBuilder(AcceptanceBuilder):

    def __init__(self):
        logger.debug("Apertura Data Provider AnagraficaInfocamere... ")
        self.dp = AnagraficaInfocamere()
        self.dp_file_extension = "xlsx"
        self.column_number = 48
        self.column_types = [np.dtype('O') for i in range(48)]
        self.column_types[10] = np.dtype('<M8[ns]')
        self.column_types[11] = np.dtype('<M8[ns]')
        self.column_types[12] = np.dtype('<M8[ns]')
        self.column_types[13] = np.dtype('<M8[ns]')
        self.column_types[14] = np.dtype('<M8[ns]')
        self.column_types[15] = np.dtype('<M8[ns]')
        self.column_types[16] = np.dtype('<M8[ns]')
        self.column_types[17] = np.dtype('<M8[ns]')
        self.column_types[18] = np.dtype('<M8[ns]')
        self.column_types[26] = np.dtype('int64')
        self.column_types[28] = np.dtype('int64')
        self.column_types[31] = np.dtype('float64')
        self.column_max_length = {
            0: 11,
            1: 6,
            2: 20,
            3: 10,
            4: 10,
            5: 20,
            6: 10,
            7: 2,
            8: 255,
            9: 50,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None,
            18: None,
            19: 255,
            20: 100,
            21: 20,
            22: 5,
            23: 100,
            24: 100,
            25: 255,
            26: None,
            27: 10,
            28: None,
            29: 11,
            30: 20,
            31: None,
            32: 255,
            33: 30,
            34: 20,
            35: 50,
            36: 50,
            37: 50,
            38: 50,
            39: 50,
            40: None,
            41: None,
            42: None,
            43: None,
            44: 20,
            45: 20,
            46: 20,
            47: 70
        }
        self.column_nullables = {i: True for i in range(48)}
        self.column_nullables[0] = False
        self.column_nullables[1] = False
        self.column_nullables[4] = False
