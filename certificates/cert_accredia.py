from certificates import Certificazioni
from data_provider import Accredia
from idb import Anagrafica

class CertificazioniAccredia(Certificazioni):

    def __init__(self):
        # Load dataprovider file
        cf_list = Anagrafica().get_fiscalcode_list()
        self.dp = Accredia()
        self.dp.set_filtred_fiscal_codes_dataframe(cf_list)

        # Load database connection
        pass