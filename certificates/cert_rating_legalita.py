from data_provider import RatingLegalita
from certificates import Certificazioni
from idb import Anagrafica

import numpy as np

class CertificazioniRatingLegalita(Certificazioni):

    def __init__(self):
        cf_list = Anagrafica().get_fiscalcode_list()
        self.dp = RatingLegalita()
        self.dp.set_filtred_fiscal_codes_dataframe(cf_list)
        self.dp_file_extension = "xlsx"
        self.column_number = 8
        self.column_types = [
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('<M8[ns]'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('<M8[ns]')
        ]
        self.column_max_length = {
            0: 20,
            1: 11,
            2: None,
            3: None,
            4: None,
            5: 50,
            6: 50,
            7: None
        }
        self.column_nullables = {
            0: True,
            1: True,
            2: True,
            3: True,
            4: True,
            5: True,
            6: True,
            7: True
        }