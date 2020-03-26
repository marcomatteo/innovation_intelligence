"""
Marco Matteo Buzzulini
26/03/2020
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

from data_providers.aiuti_di_stato import Aiuti, Componenti, Strumenti
from data_providers import DataProvider

class ParserAiutoDiStato(DataProvider):
    # Default marker for xml tags
    mark = '{http://www.rna.it/RNA_aiuto/schema}'
    # Active dir
    file_path = DataProvider.file_path + r"Aiuti_di_stato/dati/"    
    
    def __init__(self, file_name):
        self.source_file = self.file_path + file_name

        if not os.path.isfile(self.source_file):
            raise FileNotFoundError("The file not exist")
        print("Trying to parse the file: {}".format(self.source_file), end="\t")

        self.load_AiutoDiStato()
        print(".", end=" ")

        try:
            self.parseXML()
        except ET.ParseError:
            print("ERROR: can't read the XML file, remove special characters")
            exit()
        print(".", end=" ")
        
        self.getDataFrame()
        print(".", end=" ")

        print("OK")

    def getDataFrame(self):
        """Building a pandas.DataFrame"""
        aiuti_df = pd.DataFrame(self.aiuto.columns_dict).set_index('pk_aiuto')
        componenti_df = pd.DataFrame(self.componenti.columns_dict).set_index('pk_componente_aiuto')
        strumenti_df = pd.DataFrame(self.strumenti.columns_dict).set_index('pk_strumento_aiuto')
        # Merge all
        self.df = strumenti_df.merge(
            componenti_df.merge(
                aiuti_df, 
                left_on="fk_componente_aiuto",
                right_index=True
            ),
            left_on="fk_strumento_aiuto",
            right_index=True
        ) 
        # Data cleaning
        self.df.drop(columns="fk_componente_aiuto", inplace=True)
        self.df.drop(columns="fk_strumento_aiuto", inplace=True)

    def load_AiutoDiStato(self):
        self.aiuto = Aiuti()
        self.componenti = Componenti()
        self.strumenti = Strumenti()

    def addNewElement(self, tag: str, content: str):
        # AIUTI
        if tag in self.aiuto.tags:
            self.aiuto.addValueToTagColumn(
                    tag = tag, 
                    content = content
                )
        # COMPONENTI
        elif tag in self.componenti.tags:
            self.componenti.addValueToTagColumn(
                    tag = tag, 
                    content = content, 
                    foreign_index = self.aiuto.primary_index
                )
        # STRUMENTI
        elif tag in self.strumenti.tags:
            self.strumenti.addValueToTagColumn(
                    tag = tag, 
                    content = content, 
                    foreign_index = self.componenti.primary_index
                )

    def parseXML(self):
        '''
        XML Parser for OpenData_Aiuti_YEAR_MONTH.xml
        '''
        # parse XML file
        tree = ET.parse(self.source_file)
        # Reading the XML tree
        root = tree.getroot()
        for elem in root.iter():
            tag = elem.tag[len(self.mark):]
            content = elem.text
            self.addNewElement(tag, content)

if __name__ == '__main__':
    try:
        aiuti = ParserAiutoDiStato("OpenData_Aiuti_2019_08.xml")
    except FileNotFoundError:
        print("File not found")
    print("Shape and quick view: ", aiuti.df.shape)
    print(aiuti.df.head())