from data_provider import ContrattiRete
from acceptance_builder import AcceptanceBuilder

import numpy as np


class ContrattiReteBuilder(AcceptanceBuilder):

    def __init__(self):
        self.dp = ContrattiRete()

        self.dp_file_extension = "xlsx"
        self.column_number = 19

        self.columns = [
            AcceptanceBuilder.Columns(nome='progr.', tipologia=np.dtype('int64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='denominazione contratto', tipologia=np.dtype('O'), lunghezza=255, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='data atto', tipologia=np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='numero repertorio', tipologia=np.dtype('O'), lunghezza=50, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='numero atto', tipologia=np.dtype('O'), lunghezza=20, nullable=False, pk=False),
            AcceptanceBuilder.Columns(nome='oggetto', tipologia=np.dtype('O'), lunghezza=8000, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='n.rea', tipologia=np.dtype('O'), lunghezza=10, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='c.f.', tipologia=np.dtype('O'), lunghezza=16, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='denominazione impresa', tipologia=np.dtype('O'), lunghezza=8000, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='impresa di riferimento', tipologia=np.dtype('O'), lunghezza=1, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='comune', tipologia=np.dtype('O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='REG', tipologia=np.dtype('O'), lunghezza=2, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='PV', tipologia=np.dtype('O'), lunghezza=2, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='NG', tipologia=np.dtype('O'), lunghezza=2, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='codice ATECO 2007', tipologia=np.dtype('O'), lunghezza=6, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='settore attivita\'', tipologia=np.dtype('O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='sezione attivita\'', tipologia=np.dtype('O'), lunghezza=8000, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='attivita\'', tipologia=np.dtype('O'), lunghezza=8000, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='SoggettoGiuridico', tipologia=np.dtype('O'), lunghezza=2, nullable=True, pk=False)
        ]
