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

from innovation_intelligence.data_providers.dataprovider import Data

class AiutiStato(Data):
    mark = '{http://www.rna.it/RNA_aiuto/schema}'

    aiuti_tags = [
        'AIUTO', # 0: Tag di controllo
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
        'COMPONENTE_AIUTO', # 0: Tag di controllo
        # info sull'aiuto
        'ID_COMPONENTE_AIUTO', 'COD_PROCEDIMENTO', 'DES_PROCEDIMENTO', 
        'COD_REGOLAMENTO', 'DES_REGOLAMENTO', 'COD_OBIETTIVO', 
        'DES_OBIETTIVO', 'SETTORE_ATTIVITA'
    ]
    strumenti_tags = [
        'STRUMENTO_AIUTO', # 0: Tag di controllo
        # info sullo strumento dell'aiuto 
        'COD_STRUMENTO', 'DES_STRUMENTO', 'ELEMENTO_DI_AIUTO'
    ]

    def __init__(self):
        pass

    def parseXML(self, file_name):
        '''
        XML Parser.
    
        Return a matrix ECG of size n.channels * n.samples
        '''
        aiuti_dict = defaultdict(list)
        counter_aiuti_dict = defaultdict(int)
        componenti_dict = defaultdict(list)
        counter_componenti_dict = defaultdict(int)
        strumenti_dict = defaultdict(list)
        counter_strumenti_dict = defaultdict(int)

        #TODO: vedere se ritornare questa lista di tags
        tag_list = list()

        aiuti_idx = 0
        componenti_idx = 0
        strumenti_idx = 0

        tree = ET.parse(file_name)
        root = tree.getroot()

        for elem in root.iter():
            tag = elem.tag[len(self.mark):]
            tag_list.append(tag)
            content = elem.text
            aiuti_dict, counter_aiuti_dict, aiuti_idx = self.addNewColumnToDict(
                aiuti_dict, counter_aiuti_dict, self.aiuti_tags,
                tag, content, aiuti_idx
            )
            componenti_dict, counter_componenti_dict, componenti_idx = self.addNewColumnToDict(
                componenti_dict, counter_componenti_dict, self.componenti_tags,
                tag, content, componenti_idx, aiuti_idx
            )
            strumenti_dict, counter_strumenti_dict, strumenti_idx = self.addNewColumnToDict(
                strumenti_dict, counter_strumenti_dict, self.strumenti_tags,
                tag, content, strumenti_idx, componenti_idx
            )

        tag_list = set(tag_list)

        #TODO: vedere come ritornare i valori per la funzione di parsing
        return True
    
    @classmethod
    def addNewColumnToDict( cls,
            columns_dict: dict, counter_dict: dict, 
            tag_list: list, tag: str, content: str, 
            primary_index: int, foreign_index: int = None
        ) -> tuple(dict, dict, int):
        """
        The method adds a new column value into a dictionary
        with counter checking for feature parsing into 
        pandas.DataFrame object.
        """
        if tag == tag_list[0]:
            columns_dict, counter_dict = cls.fillDictForDataFrame(
                columns_dict, counter_dict, primary_index
            )
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

    @classmethod
    def checkCounterDict(cls, 
            data: dict, counter: int
        ) -> list:
        """
        Check if every key in the dict as the same number,
        if not return the keys in a list
        
        Attributes:
        -----------
            data: dictionary
            
            count: int
        
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
        ) -> tuple(dict, dict):
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