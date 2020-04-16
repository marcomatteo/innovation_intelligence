from certificates import Certificazioni
from data_provider import Modefinance

class CertificazioniModefinance(Certificazioni):
    
    def __init__(self):
        self.dp = Modefinance()