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

class AiutiDiStato(DataProvider):
    """
    Classe di Data Provider per gli Aiuti di Stato disponibili dagli OPEN DATA.

    Negli OPEN DATA sono disponibili le informazioni 
    sui finanziamenti rivolti alle imprese, espressi come aiuti individuali

    Gli AIUTI sono memorizzati in un file XML, con diversi tag.
    I tag sono stati raggruppati in 3 dizionari definiti come:

        1. aiuti_tags: Informazioni sul bando o legge per il finanziamento

        2. componenti_tags: regolamento e tipologia (ex notifica, esenzione, de minimis)

        3. strumenti_tags: informazioni sull'aiuto erogato (importo, forma finanziamento)

    I dizionari vengono poi convertiti in un pandas.DataFrame

    Relazioni tra i vari dizionari:

        - aiuti_tags [1]->[N] componenti_tags

        - componenti_tags [1]->[N] strumenti_tags
    """
    mark = '{http://www.rna.it/RNA_aiuto/schema}'

    aiuti_tags = [
        'AIUTO', # 0: Tag di nuovo record
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
    componenti_tags = [
        'COMPONENTE_AIUTO', # 0: Tag di nuovo record
        # info sull'aiuto
        'ID_COMPONENTE_AIUTO', 'COD_PROCEDIMENTO', 'DES_PROCEDIMENTO', 
        'COD_REGOLAMENTO', 'DES_REGOLAMENTO', 'COD_OBIETTIVO', 
        'DES_OBIETTIVO', 'SETTORE_ATTIVITA'
    ]
    strumenti_tags = [
        'STRUMENTO_AIUTO',  # 0: Tag di nuovo record
        # info sullo strumento dell'aiuto 
        'COD_STRUMENTO',    # Codice nel registro
        'DES_STRUMENTO',    # Forma in cui viene concesso l'aiuto
        'ELEMENTO_DI_AIUTO' # Importo dell'aiuto
    ]

    columns_dict = defaultdict(list)
    counter_dict = defaultdict(int)

    @staticmethod
    def checkCounterDict( 
            data: dict, counter: int
        ) -> list:
        """
        Metodo che permette di controllare se
        ci sono disallineamenti nel dict contatore.
        Ritorna le keys nel dict che hanno un numero di
        campi inferiore a counter.
        
        Attributes:
        -----------
            data: dict
            dizionario che associa le informazioni in coppia 
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
            
    @classmethod
    def fillDictForDataFrame(cls, 
            columns_dict: dict, count_dict: dict, num: int
        ) -> (dict, dict):
        """
        Fill the counter to count for every key,
        return the data dict filled
        
        Attributes:
        -----------
            data: dictionary
            
            count: int
        
        Return:
        -------
            dict

            dict
        """
        keys = cls.checkCounterDict(count_dict, num)
        
        if not keys:
            # Nothing to append
            return columns_dict, count_dict
        
        for key in keys:
            # Append None and update the counter
            while count_dict[key] < num:
                columns_dict[key].append(None)
                count_dict[key] += 1
                
        return columns_dict, count_dict 

    def __init__(self, year):
        self.file_path = self.file_path + r"Aiuti_di_stato/dati/" + \
                str(year) + r"/"
        
        if not os.path.isdir(self.file_path):
            raise ValueError("Argument year not in /Aiuti_di_stato/dati/")

        #TODO: utilizzare funzione parseXML per ogni file nella cartella year
        #TODO: assemblare ogni DataFrame per crearne uno univoco per l'anno
        #TODO: decidere come strutturare le informazioni (3 DataFrames?)


    def parseXML_Aiuti(self, file_name):
        '''
        XML Parser for OpenData_Aiuti_YEAR_MONTH.xml
        '''
        # Dict per 
        aiuti_dict = defaultdict(list)
        counter_aiuti_dict = defaultdict(int)
        componenti_dict = defaultdict(list)
        counter_componenti_dict = defaultdict(int)
        strumenti_dict = defaultdict(list)
        counter_strumenti_dict = defaultdict(int)
        # Indici per costruire dati omogenei
        aiuti_idx = 0
        componenti_idx = 0
        strumenti_idx = 0

        # XML external libraries
        try:
            tree = ET.parse(file_name)
        except ET.ParseError:
            raise ValueError("Bad XML file")

        # Reading the file
        root = tree.getroot()
        for elem in root.iter():
            tag = elem.tag[len(self.mark):]
            content = elem.text
            # AIUTI
            aiuti_dict, counter_aiuti_dict, aiuti_idx = self.addNewColumnToDict(
                    columns_dict = aiuti_dict, 
                    counter_dict = counter_aiuti_dict, 
                    tag_list = self.aiuti_tags,
                    tag = tag, 
                    content = content, 
                    primary_index = aiuti_idx
                )
            # COMPONENTI
            componenti_dict, counter_componenti_dict, componenti_idx = self.addNewColumnToDict(
                    columns_dict = componenti_dict, 
                    counter_dict = counter_componenti_dict, 
                    tag_list = self.componenti_tags,
                    tag = tag, 
                    content = content, 
                    primary_index = componenti_idx, 
                    foreign_index = aiuti_idx
                )
            # STRUMENTI
            strumenti_dict, counter_strumenti_dict, strumenti_idx = self.addNewColumnToDict(
                    columns_dict = strumenti_dict, 
                    counter_dict = counter_strumenti_dict, 
                    tag_list = self.strumenti_tags,
                    tag = tag, 
                    content = content, 
                    primary_index = strumenti_idx, 
                    foreign_index = componenti_idx
                )
                
        return True
    
    @classmethod
    def addNewColumnToDict( cls,
            columns_dict: dict, counter_dict: dict, 
            tag_list: list, tag: str, content: str, 
            primary_index: int, foreign_index: int = None
        ) -> (dict, dict, int):
        """
        The method adds a new column value into a dictionary
        with counter checking for feature parsing into 
        pandas.DataFrame object.
        """
        # Il primo tag indica che si crea un nuovo record
        if tag == tag_list[0]:
            # Controllo che il record precedente abbia tutti i campi
            columns_dict, counter_dict = cls.fillDictForDataFrame(
                columns_dict, counter_dict, primary_index
            )
            # Creo chiave primaria
            key = 'pk_' + str(tag).lower()
            columns_dict[key].append(primary_index)
            if foreign_index:
                key = 'fk_' + str(tag).lower()
                columns_dict[key].append(foreign_index)
            primary_index += 1
        elif tag in tag_list:
            columns_dict[tag].append(content)
            counter_dict[tag] += 1
            
        return columns_dict, counter_dict, primary_index

if __name__ == '__main__':
    aiuti = AiutiDiStato(2019)