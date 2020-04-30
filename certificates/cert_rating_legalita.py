from data_provider import RatingLegalita
from certificates import Certificazioni
from idb import Anagrafica

class CertificazioniRatingLegalita(Certificazioni):

    def __init__(self):
        cf_list = Anagrafica().get_fiscalcode_list()
        self.dp = RatingLegalita()
        self.dp.set_filtred_fiscal_codes_dataframe(cf_list)