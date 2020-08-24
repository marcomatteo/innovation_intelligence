from data_provider import ContrattiRete
from acceptance_builder import AcceptanceBuilder

import numpy as np


class ContrattiReteBuilder(AcceptanceBuilder):

    def __init__(self):
        self.dp = ContrattiRete()

        self.dp_file_extension = "xlsx"
        self.column_number = 19

        self.columns = [
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'int64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=255, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                '<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=50, nullable=False, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=20, nullable=False, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=8000, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=10, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=16, nullable=False, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=8000, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=1, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=2, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=2, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=2, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=6, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=8000, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=8000, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='', tipologia=np.dtype(
                'O'), lunghezza=2, nullable=True, pk=False)
        ]
