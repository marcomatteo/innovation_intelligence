from acceptance_builder import AcceptanceBuilder
from data_provider import AtecoInsiel

import numpy as np

class AtecoInsielBuilder(AcceptanceBuilder):
    
    def __init__(self):
        self.dp = AtecoInsiel()
        self.dp_file_extension = "xlsx"
        self.column_number = 7
        self.columns = [
            AcceptanceBuilder.Columns(nome='c fiscale', tipologia=np.dtype('O'), lunghezza=11, nullable=False, pk=False),
            AcceptanceBuilder.Columns(nome='pv', tipologia=np.dtype('O'), lunghezza=6, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='rea', tipologia=np.dtype('O'), lunghezza=10, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='loc', tipologia=np.dtype('int64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='imp att', tipologia=np.dtype('O'), lunghezza=1, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='ateco 2007', tipologia=np.dtype('O'), lunghezza=10, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='descrizione ateco 2007', tipologia=np.dtype('O'), lunghezza=200, nullable=True, pk=False)
        ]
