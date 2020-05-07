from certificates import Certificazioni
from data_provider import Accredia
from idb import Anagrafica

import numpy as np

class CertificazioniAccredia(Certificazioni):

    def __init__(self):
        # Load dataprovider file
        cf_list = Anagrafica().get_fiscalcode_list()
        
        self.dp = Accredia()
        self.dp.set_filtred_fiscal_codes_dataframe(cf_list)

        #TODO: Load database connection
        self.dp_file_extension = "csv"
        self.column_number = 5
        self.column_types = [
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('O'),
            np.dtype('int64'),
            np.dtype('O')
        ]
        self.column_max_length = {
            0: 19,
            1: 6,
            2: 50,
            3: None,
            4: 2
        }
        self.column_nullables = {
            0: False,
            1: True,
            2: True,
            3: True,
            4: True
        }
        pass