from acceptance_builder import AcceptanceBuilder
from data_provider import AnagraficaInfocamere

import numpy as np

class AnagraficaBuilder(AcceptanceBuilder):

    def __init__(self):
        self.dp = AnagraficaInfocamere()
        self.dp.df = self.dp.df.iloc[:,  list(self.column_constraints.keys())]
        self.dp_file_extension = "xlsx"
        self.column_number = 48
        self.columns = [
            AcceptanceBuilder.Columns(nome='c fiscale', tipologia= np.dtype('O'), lunghezza=11, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='PRV - Provincia', tipologia= np.dtype('O'), lunghezza=6, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='N-REG-IMP - Numero Registro Imprese', tipologia= np.dtype('O'), lunghezza=20, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='rea', tipologia= np.dtype('O'), lunghezza=10, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='UL-SEDE - Unità Locale o sede dell\'impresa', tipologia= np.dtype('O'), lunghezza=10, nullable=False, pk=True),
            AcceptanceBuilder.Columns(nome='N-ALBO-AA - Numero di iscrizione all\'Albo Imprese Artigiane', tipologia= np.dtype('O'), lunghezza=20, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='SEZ-REG-IMP - Sezione di iscrizione dell\'impresa al Registro del', tipologia= np.dtype('O'), lunghezza=10, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='NG - Natura Giuridica', tipologia= np.dtype('O'), lunghezza=2, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='natura giuridica', tipologia= np.dtype('O'), lunghezza=255, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='tipo impresa', tipologia= np.dtype('O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='DT-ISCR-RI - Data di iscrizione al Registro Imprese', tipologia= np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='DT-ISCR-RD - Data di iscrizione al Registro delle Ditte', tipologia= np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='DT-ISCR-AA - Data di iscrizione all\'Albo delle Imprese Artigiane', tipologia= np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='DT-APER-UL - Data di apertura dell\'Unità Locale', tipologia= np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='cancellazione', tipologia= np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='DT-INI-AT - Data di inizio attività dell\'impresa', tipologia= np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='dt cessazione attività', tipologia= np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='fallimento', tipologia= np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='DT-LIQUID - Data liquidazione dell\'impresa', tipologia= np.dtype('<M8[ns]'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='DENOMINAZIONE - Denominazione dell\'impresa', tipologia= np.dtype('O'), lunghezza=255, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='INDIRIZZO', tipologia= np.dtype('O'), lunghezza=100, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='STRAD - Via', tipologia= np.dtype('O'), lunghezza=20, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='CAP', tipologia= np.dtype('O'), lunghezza=5, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='COMUNE', tipologia= np.dtype('O'), lunghezza=100, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='FRAZIONE', tipologia= np.dtype('O'), lunghezza=100, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='ALTRE-INDICAZIONI - Altre indicazioni relative all\'indirizz del', tipologia= np.dtype('O'), lunghezza=255, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='AA-ADD - Anno di dichiarazione degli addetti', tipologia= np.dtype('int64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='IND - Numero addetti indipendenti', tipologia= np.dtype('O'), lunghezza=10, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='DIP - Numero addetti dipendenti', tipologia= np.dtype('int64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='PARTITA IVA', tipologia= np.dtype('O'), lunghezza=11, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='TELEFONO', tipologia= np.dtype('O'), lunghezza=20, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='CAPITALE - Capitale sociale dell\'impresa', tipologia= np.dtype('float64'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='ATTIVITA\' - Descrizione dell\'attività principale dell\'impresa', tipologia= np.dtype('O'), lunghezza=255, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='VALUTA-CAPITALE - Valuta del capitale sociale dell\'impresa', tipologia= np.dtype('O'), lunghezza=30, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='stato impresa/ul', tipologia= np.dtype('O'), lunghezza=20, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='tipo sede/ul1', tipologia= np.dtype('O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='tipo sede/ul2', tipologia= np.dtype('O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='tipo sede/ul3', tipologia= np.dtype('O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='tipo sede/ul4', tipologia= np.dtype('O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='tipo sede/ul5', tipologia= np.dtype('O'), lunghezza=50, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Presenza di sedi secondarie all\'estero', tipologia= np.dtype('O'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Impresa estera con unità locale in Friuli Venezia Giulia', tipologia= np.dtype('O'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='sezione Impresa - Indicazione delle imprese che sono PMI', tipologia= np.dtype('O'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='sezione Impresa - Indicazione delle imprese che sono start up', tipologia= np.dtype('O'), lunghezza=None, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Impr Femminile', tipologia= np.dtype('O'), lunghezza=20, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Impr Giovane', tipologia= np.dtype('O'), lunghezza=20, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='Impr Straniera', tipologia= np.dtype('O'), lunghezza=20, nullable=True, pk=False),
            AcceptanceBuilder.Columns(nome='pec', tipologia= np.dtype('O'), lunghezza=70, nullable=True, pk=False)
        ]
