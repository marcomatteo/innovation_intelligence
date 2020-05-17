"""
Created 06/02/2020

"""

import numpy as np
import pandas as pd
import os
from collections import defaultdict
from collections import Counter
import sys
sys.path.append(
    r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")


class AiutoDiStato:
    """
    Classe di Data Provider per gli Aiuti di Stato disponibili dagli OPEN DATA.

    Negli OPEN DATA sono disponibili le informazioni 
    sui finanziamenti rivolti alle imprese, espressi come aiuti individuali

    Gli AIUTI sono memorizzati in un file XML, con diversi tag.
    I tag sono stati raggruppati in 3 dizionari definiti come:

        1. Aiuti: Informazioni sul bando o legge per il finanziamento

        2. Componenti: regolamento e tipologia (ex notifica, esenzione, de minimis)

        3. Strumenti: informazioni sull'aiuto erogato (importo, forma finanziamento)

    I dizionari vengono poi convertiti in un pandas.DataFrame

    Relazioni tra i vari dizionari:

        - Aiuti [1]->[N] Componenti

        - Componenti [1]->[N] Strumenti
    """
    tags = list()

    def __init__(self):
        self.columns_dict = defaultdict(list)
        self.counter_dict = defaultdict(int)
        self.primary_index = 0

    @staticmethod
    def check_dict_counter(
        data: dict, counter: int
    ) -> list:
        """
        Metodo che permette di controllare se \
        ci sono disallineamenti nel dict contatore. \
        Ritorna le keys nel dict che hanno un numero di \
        campi inferiore a counter.

        Attributes:
        -----------
            data: dict
            dizionario che associa le informazioni in coppia \
            di (key, value) che identificano le informazioni sugli aiuti 

                - key: tag del file XML

                - value: contatore del campo corrispondente al tag

            count: int
            numero intero 

        Return:
        -------
            list
        """
        returned = list()
        for key, val in data.items():
            if val < counter:
                returned.append(key)
        return returned

    def check_column_values(self, num: int):
        """
        Metodo che controlla che tutti i valori
        abbiano lo stesso conteggio per integrità dei dati
        e conversione in pandas.DataFrame

        Attributes:
        -----------
            num: int
            Il numero di conteggio che dovrebbe essere 
            uguale in ogni valore del dizionario contatore
        """
        keys = self.check_dict_counter(self.counter_dict, num)

        if keys:
            for key in keys:
                # Append None and update the counter
                while self.counter_dict[key] < num:
                    self.columns_dict[key].append(None)
                    self.counter_dict[key] += 1

    def add_value_to_tag_column(self,
                                tag: str, content: str,
                                foreign_index: int = None):
        """
        Metodo che aggiunge un nuovo valore al tag
        della fattispecie di AiutoDiStato che richiama 
        il metodo (se presente).

        Attributes:
        -----------
            tag: str
            Il tag XML a cui aggiungere il nuovo valore

            content: str
            Il contenuto/valore da aggiungere

            foreign_index: int, Default=None
            La chiave esterna per rispettare la relazione
            esistente tra gli oggetti di AiutoDiStato
        """
        # Nuova riga
        if tag == self.tags[0]:
            self.check_column_values(self.primary_index)

            key = 'pk_' + str(tag).lower()
            self.columns_dict[key].append(self.primary_index)

            self.primary_index += 1

            # Aggiungo riferimento esterno, se presente
            if foreign_index:
                key = 'fk_' + str(tag).lower()
                self.columns_dict[key].append(foreign_index)

        # inserisco valore colonna
        elif tag in self.tags:
            self.columns_dict[tag].append(content)
            self.counter_dict[tag] += 1

    def get_counter_values(self):
        for num, (key, val) in enumerate(self.columns_dict.items()):
            print(num, key, len(val))


class Aiuti(AiutoDiStato):

    tags = [
        # Tag di nuovo record
        'AIUTO',
        # info sulla misura collegata
        'CAR', 'TITOLO_MISURA', 'DES_TIPO_MISURA',
        # info sui soggetti legati alla misura
        'BASE_GIURIDICA_NAZIONALE', 'LINK_TESTO_INTEGRALE_MISURA',
        'COD_UFF_GESTORE', 'DENOMINAZIONE_UFF_GESTORE', 'SOGGETTO_CONCEDENTE',
        # info sull'aiuto
        'COR', 'TITOLO_PROGETTO', 'DESCRIZIONE_PROGETTO',
        'DATA_CONCESSIONE', 'CUP', 'ATTO_CONCESSIONE',
        # info sul soggetto beneficiario dell'aiuto
        'DENOMINAZIONE_BENEFICIARIO', 'CODICE_FISCALE_BENEFICIARIO',
        'DES_TIPO_BENEFICIARIO', 'REGIONE_BENEFICIARIO'
    ]

    def __init__(self):
        super().__init__()


class Componenti(AiutoDiStato):

    tags = [
        # Tag di nuovo record
        'COMPONENTE_AIUTO',
        'ID_COMPONENTE_AIUTO',
        'COD_PROCEDIMENTO',
        'DES_PROCEDIMENTO',
        'COD_REGOLAMENTO',
        'DES_REGOLAMENTO',
        'COD_OBIETTIVO',
        'DES_OBIETTIVO',
        'SETTORE_ATTIVITA'
    ]

    def __init__(self):
        super().__init__()


class Strumenti(AiutoDiStato):

    tags = [
        # Tag di nuovo record
        'STRUMENTO_AIUTO',
        # Codice nel registro
        'COD_STRUMENTO',
        # Forma in cui viene concesso l'aiuto
        'DES_STRUMENTO',
        # Importo dell'aiuto
        'ELEMENTO_DI_AIUTO'
    ]

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    pass
