"""
Created 06/02/2020

"""

import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import json
import os
from collections import defaultdict
from collections import Counter
import sys
sys.path.append(r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")

from data_providers import DataProvider

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

    def set_column_tag(self, 
        tag: str, content: str,
        foreign_index: int = None):
        """
        The method adds a new column value into a dictionary
        with counter checking for feature parsing into 
        pandas.DataFrame object.
        """
        # Il primo tag indica che si crea un nuovo record
        if tag == self.tags[0]:
            # Controllo che il record precedente abbia tutti i campi
            self.check_column_values(self.primary_index)
            # Creo chiave primaria
            key = 'pk_' + str(tag).lower()
            self.columns_dict[key].append(self.primary_index)
            if foreign_index:
                key = 'fk_' + str(tag).lower()
                self.columns_dict[key].append(foreign_index)
            self.primary_index += 1
        elif tag in self.tags:
            self.columns_dict[tag].append(content)
            self.counter_dict[tag] += 1

    def get_counter_values(self):
        for num, (key, val) in enumerate(self.columns_dict.items()):
            print(num, key, len(val))

    def __init__(self):
        self.columns_dict = defaultdict(list)
        self.counter_dict = defaultdict(int)
        self.primary_index = 0

class Aiuti(AiutoDiStato):
    
    tags = [
        'AIUTO', # Tag di nuovo record
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
        self.columns_dict = defaultdict(list)
        self.counter_dict = defaultdict(int)
        self.primary_index = 0

class Componenti(AiutoDiStato):
    
    tags = [
        'COMPONENTE_AIUTO', # Tag di nuovo record
        # info sull'aiuto
        'ID_COMPONENTE_AIUTO', 'COD_PROCEDIMENTO', 'DES_PROCEDIMENTO', 
        'COD_REGOLAMENTO', 'DES_REGOLAMENTO', 'COD_OBIETTIVO', 
        'DES_OBIETTIVO', 'SETTORE_ATTIVITA'
    ]

    def __init__(self):
        self.columns_dict = defaultdict(list)
        self.counter_dict = defaultdict(int)
        self.primary_index = 0
    
class Strumenti(AiutoDiStato):

    tags = [
        'STRUMENTO_AIUTO',  # Tag di nuovo record
        # info sullo strumento dell'aiuto 
        'COD_STRUMENTO',    # Codice nel registro
        'DES_STRUMENTO',    # Forma in cui viene concesso l'aiuto
        'ELEMENTO_DI_AIUTO' # Importo dell'aiuto
    ]

    def __init__(self):
        self.columns_dict = defaultdict(list)
        self.counter_dict = defaultdict(int)
        self.primary_index = 0
    
class ParserAiuto(DataProvider):
    mark = '{http://www.rna.it/RNA_aiuto/schema}'

    def parseXML(self):
        '''
        XML Parser for OpenData_Aiuti_YEAR_MONTH.xml
        '''
        # XML external libraries
        tree = ET.parse(self.source_file)

        # Reading the file
        root = tree.getroot()
        for elem in root.iter():
            tag = elem.tag[len(self.mark):]
            content = elem.text
            # AIUTI
            self.aiuto.set_column_tag(
                    tag = tag, 
                    content = content
                )
            # COMPONENTI
            self.componenti.set_column_tag(
                    tag = tag, 
                    content = content, 
                    foreign_index = self.aiuto.primary_index
                )
            # STRUMENTI
            self.strumenti.set_column_tag(
                    tag = tag, 
                    content = content, 
                    foreign_index = self.componenti.primary_index
                )

    def __init__(self, file_name):
        self.file_path = self.file_path + r"Aiuti_di_stato/dati/"
        self.file_name = file_name
        self.source_file = self.file_path + self.file_name

        if not os.path.isfile(self.source_file):
            raise FileNotFoundError("The file not exist")
        print(self.source_file)

        self.aiuto = Aiuti()
        self.componenti = Componenti()
        self.strumenti = Strumenti()

        try:
            self.parseXML()
        except ET.ParseError:
            print("Error: can't read the XML file")
            exit()

        aiuti_df = pd.DataFrame(self.aiuto.columns_dict).set_index('pk_aiuto')
        componenti_df = pd.DataFrame(self.componenti.columns_dict).set_index('pk_componente_aiuto')
        strumenti_df = pd.DataFrame(self.strumenti.columns_dict).set_index('pk_strumento_aiuto')

        self.df = strumenti_df.merge(
            componenti_df.merge(
                aiuti_df, 
                left_on="fk_componente_aiuto",
                right_index=True
            ),
            left_on="fk_strumento_aiuto",
            right_index=True
        )        
        self.df.drop(columns="fk_componente_aiuto", inplace=True)
        self.df.drop(columns="fk_strumento_aiuto", inplace=True)

if __name__ == '__main__':
    try:
        aiuti = ParserAiuto("OpenData_Aiuti_2019_08.xml")
    except FileNotFoundError:
        print("File not found")
    print(aiuti.df.shape)
    print(aiuti.df.head())