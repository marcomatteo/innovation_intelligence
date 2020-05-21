"""
Marco Matteo Buzzulini
26/03/2020
"""

from data_providers.aiuti_di_stato import Aiuti, Componenti, Strumenti
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import json
import os
from collections import defaultdict
from collections import Counter
import sys
sys.path.append(
    r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence")


class ParserAiutoDiStato:
    # Default marker for xml tags
    mark = '{http://www.rna.it/RNA_aiuto/schema}'

    def __init__(self, file_name):
        self.source_file = file_name

        self.setup_objects()

        try:
            self.parse_xml()
        except ET.ParseError:
            print("ERROR: can't read the XML file, try removing special characters")
            exit()
        except FileNotFoundError:
            print("File not found!")
        else:
            print(".", end=" ")

        self.df = self.get_dataframe_from_objs()

    def setup_objects(self):
        self.aiuto = Aiuti()
        self.componenti = Componenti()
        self.strumenti = Strumenti()

    def parse_xml(self):
        '''
        XML Parser for OpenData_Aiuti_YEAR_MONTH.xml
        '''
        if not os.path.isfile(self.source_file):
            raise FileNotFoundError("The file not exist")
        else:
            print("Trying to parse the file: {}".format(
                self.source_file), end="\t")

        # parse XML file
        tree = ET.parse(self.source_file)

        # Reading the XML tree
        root = tree.getroot()

        for elem in root.iter():
            tag = elem.tag[len(self.mark):]
            content = elem.text

            self.add_xlm_content_to_objs(tag, content)

    def add_xlm_content_to_objs(self, tag: str, content: str):
        # AIUTI
        if tag in self.aiuto.tags:
            self.aiuto.add_value_to_tag_column(
                tag=tag,
                content=content
            )
        
        # COMPONENTI
        elif tag in self.componenti.tags:
            self.componenti.add_value_to_tag_column(
                tag=tag,
                content=content,
                foreign_index=self.aiuto.primary_index
            )
        
        # STRUMENTI
        elif tag in self.strumenti.tags:
            self.strumenti.add_value_to_tag_column(
                tag=tag,
                content=content,
                foreign_index=self.componenti.primary_index
            )

    def get_dataframe_from_objs(self) -> pd.DataFrame:
        """
        Building a pandas.DataFrame
        """
        
        aiuti_df = pd.DataFrame(self.aiuto.columns_dict).set_index('pk_aiuto')
        componenti_df = pd.DataFrame(
            self.componenti.columns_dict).set_index('pk_componente_aiuto')
        strumenti_df = pd.DataFrame(
            self.strumenti.columns_dict).set_index('pk_strumento_aiuto')

        # Merge all
        df = strumenti_df.merge(
            componenti_df.merge(
                aiuti_df,
                left_on="fk_componente_aiuto",
                right_index=True
            ),
            left_on="fk_strumento_aiuto",
            right_index=True
        )

        # Data cleaning
        df.drop(columns="fk_componente_aiuto", inplace=True)
        df.drop(columns="fk_strumento_aiuto", inplace=True)

        print(". OK")

        return df


if __name__ == '__main__':
    try:
        aiuti = ParserAiutoDiStato("OpenData_Aiuti_2019_08.xml")
    except FileNotFoundError:
        print("File not found")
    print("Shape and quick view: ", aiuti.df.shape)
    print(aiuti.df.head())
