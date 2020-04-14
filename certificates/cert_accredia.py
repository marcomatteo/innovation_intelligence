from certificates import Certificazioni
from data_provider import Accredia

import numpy as np

class CertificazioniAccredia(Certificazioni):

    def __init__(self):
        self.dp = Accredia()

if __name__ == '__main__':
    cert = CertificazioniAccredia()
    print(dir(cert))