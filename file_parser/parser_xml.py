import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import json
import os

from collections import defaultdict
from collections import Counter


class IXMLObj:
    """
    XMLObj interface

    xml_objs: lista che contiene gli oggetti XML
    """
    xml_objs: list = NotImplemented  # type: list
    mark: str = NotImplemented       # type: str

    def add_content_to_xml_objs(self, tag: str, content: str):

        for num, xml_obj in enumerate(self.xml_objs):

            if tag in xml_obj.tags:
                foreign_index = None
                if num > 0:
                    foreign_index = self.xml_objs[num - 1].primary_index

                xml_obj.add_value_to_tag_column(
                    tag=tag,
                    content=content,
                    foreign_index=foreign_index
                )

    def get_DataFrame(self):
        df_list = list()

        for xml_obj in self.xml_objs:
            df_list.append(xml_obj.get_DataFrame())

        obj_number = len(df_list)

        if obj_number == 1:
            return df_list.pop(0)

        max_merge_operations = obj_number - 1
        merge_iterator = range(max_merge_operations)
        df_merged = list(merge_iterator)

        for merge_operation in merge_iterator:
            if merge_operation == 0:
                first_df = df_list[obj_number]
            else:
                first_df = df_merged[merge_operation - 1]

            second_num = obj_number - merge_operation
            second_df = df_list[second_num]

            df_merged[merge_operation] = first_df.merge(
                second_df,
                left_on=self.xml_objs[second_num].fk_key,
                right_index=True
            ).drop(columns=self.xml_objs[second_num].fk_key)

        return df_merged.pop(max_merge_operations)


class XMLObj:
    """
    XMLObj rappresenta un oggetto presente in un file XML

    tags: lista di tag da leggere nel file XML
    """

    tags = list()

    def __init__(self, tags=None):
        self.columns_dict = defaultdict(list)
        self.counter_dict = defaultdict(int)
        self.primary_index = 0

        if tags:
            self.tags = tags

    @property
    def pk_key(self):
        """
        Ritorna la chiave primaria dell'oggetto
        """
        return "pk_" + str(self.tags[0]).lower()

    @property
    def fk_key(self):
        """
        Ritorna la chiave esterna dell'oggetto, se presente
        """
        for column in self.columns_dict.keys():
            if str(column).startswith("fk_"):
                return column

        return None

    @staticmethod
    def check_dict_counter(
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

    def check_column_values(self, num: int):
        """
        Metodo che controlla che tutti i valori
        abbiano lo stesso conteggio per integrità dei dati
        e per permette di convertire il dict in pandas.DataFrame

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
        della fattispecie di XMLObj che richiama 
        il metodo (se presente).

        Attributes:
        -----------
            tag: str
            Il tag XML a cui aggiungere il nuovo valore

            content: str
            Il contenuto/valore da aggiungere

            foreign_index: int, Default=None
            La chiave esterna per rispettare la relazione
            esistente tra gli oggetti di XMLObj
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
        """
        Stampa i valori e il conteggio dei dati nel dict dell'oggetto XML
        """
        for num, (key, val) in enumerate(self.columns_dict.items()):
            print(num, key, len(val))

    def get_DataFrame(self):
        """
        Ritorna un pandas.DataFrame dell'oggetto XML
        """
        return pd.DataFrame(self.columns_dict).set_index(self.pk_key)


class Aiuti(XMLObj):

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

    def __init__(self, tags=None):
        super().__init__(tags=tags)


class Componenti(XMLObj):

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


class Strumenti(XMLObj):

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


class AiutiDiStato(IXMLObj):
    """
    Classe per gli Aiuti di Stato di tipo XMLObj.

    GLi Aiuti di Stato sono disponibili dagli OPEN DATA e rappresentano 
    i finanziamenti rivolti alle imprese, espressi come aiuti individuali

    Gli Aiuti di Stato sono memorizzati in un file XML, con diversi tag.

    All'interno del file XML è possibile distinguere 3 diverse tipologie di informazioni, 
    descritti dalle seguenti classi:

        1. Aiuti: Informazioni sul bando o legge per il finanziamento

        2. Componenti: regolamento e tipologia (ex notifica, esenzione, de minimis)

        3. Strumenti: informazioni sull'aiuto erogato (importo, forma finanziamento)

    Relazioni tra le classi:

        - Aiuti [1]->[N] Componenti

        - Componenti [1]->[N] Strumenti

    Il pandas.DataFrame da ottenere conterrà quindi:
    --------------------------------
    |Strumenti | Componenti | Aiuti|
    --------------------------------
    """
    # Default marker for xml tags
    mark = '{http://www.rna.it/RNA_aiuto/schema}'

    def __init__(self):
        aiuti = Aiuti()
        componenti = Componenti()
        strumenti = Strumenti()

        self.xml_objs = [aiuti, componenti, strumenti]


class XMLParser:

    def __init__(self, file_name: str, xml_interface: IXMLObj):
        self.file_name = file_name
        self.xml_interface = xml_interface

        if not os.path.isfile(self.file_name):
            raise FileNotFoundError("The file not exist")
        else:
            print("Trying to parse the file: {}".format(
                self.file_name), end="\t")

    def parse_xml(self) -> pd.DataFrame:
        """
        Parse a XML file and return a pandas.DataFrame
        """
        # parse XML file
        tree = ET.parse(self.file_name)

        # Reading the XML tree
        root = tree.getroot()

        for elem in root.iter():
            tag = elem.tag[len(self.xml_interface.mark):]
            content = elem.text

            self.xml_interface.add_content_to_xml_objs(tag, content)

        return self.xml_interface.get_DataFrame()
