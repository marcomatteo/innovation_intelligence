from acceptance_builder import AcceptanceBuilder
from data_provider import BilanciInfocamere

import numpy as np

class BilanciBuilder(AcceptanceBuilder):
    
    def __init__(self):
        self.dp = BilanciInfocamere()
        self.dp.df = self.dp.df.iloc[:, :16]
        self.dp_file_extension = "xlsx"
        self.column_number = 16
        self.columns = [
            AcceptanceBuilder.Columns(nome='c fiscale', tipologia=np.dtype('O'), lunghezza=11, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='cia', tipologia=np.dtype('O'), lunghezza=6, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='rea', tipologia=np.dtype('O'), lunghezza=10, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='anno', tipologia=np.dtype('int64'), lunghezza=None, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='Totale attivo', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Totale Immobilizzazioni immateriali', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Crediti esigibili entro l\'esercizio successivo', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Totale patrimonio netto', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Debiti esigibili entro l\'esercizio successivo', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Totale valore della produzione', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Ricavi delle vendite', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Totale Costi del Personale', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Differenza tra valore e costi della produzione', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Ammortamento Immobilizzazione Immateriali', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Utile/perdita esercizio ultimi', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='valore aggiunto', tipologia=np.dtype('float64'), lunghezza=None, nullable=True, pk=False)
        ]
