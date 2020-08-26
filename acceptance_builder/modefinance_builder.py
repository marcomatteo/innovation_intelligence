from acceptance_builder import AcceptanceBuilder
from data_provider import Modefinance

import numpy as np

class ModefinanceBuilder(AcceptanceBuilder):
    
    def __init__(self):
        self.dp = Modefinance()
        self.dp_file_extension = "csv"
        self.column_number = 4
        self.columns = [
            AcceptanceBuilder.Columns(nome='fiscal_code', tipologia=np.dtype('O'), lunghezza=19, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='final_rank', tipologia=np.dtype('int64'), lunghezza=6, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='evaluation_date', tipologia=np.dtype('<M8[ns]'), lunghezza=20, nullable=True, pk=True),
            AcceptanceBuilder.Columns(nome='is_consolidated', tipologia=np.dtype('O'), lunghezza=10, nullable=True, pk=False)
        ]