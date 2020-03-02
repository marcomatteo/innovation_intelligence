"""
Creata il: 20/08/2019

Classe per la tabella DATA_Imprese di Innovation Intelligence.

Innovation Intelligence in Python
Marco Matteo Buzzulini
"""
import os

path = f"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts"
try:
    os.chdir(path)
    #print(f"Current dir: {os.getcwd()}")
except:
    print("Can't load the right dir")   

from innovation_intelligence.db_interface.i2fvg import I2FVG
import pandas as pd

class Anagrafica(I2FVG):
    # Costanti della classe Anagrafica
    _names = { 
        'sedi': "DATA_Impresa",
        'ul': "DATA_UnitaLocale"
    }

    def __init__(self, inTest = True):
        super().__init__(inTest = inTest)       
        self.open_tables()
        self.df = self.tbl_df['sedi']
        #self.df = self.get_localizzazioni()
    
    #TODO: Da modificare questa funzione 
    def get_localizzazioni(self):
        """
        Metodo che permette di ottenere la tabella di Innovation Intelligence 
        come dalla pagina report "Localizzazioni".
        Effettuo l'unione delle informazioni contenute in:
        - 'DATA_Impresa' 
        - 'DATA_UnitaLocale'
        """
        df_sedi_mod = self.tbl_df['sedi'].rename(columns={"ID_Impresa":"ID"})
        df_ul_mod = self.tbl_df['ul'].rename(columns={"ID_UnitaLocale":"ID"})
        return df_sedi_mod.loc[:, df_ul_mod.columns].append(
            df_ul_mod, ignore_index=True, sort=False)

    def find_name(self, name, status=None):
        """
        Metodo che dato un nome (anche parziale) ritorna una lista 
        di possibili aziende con il cf, nome completo e indirizzo.
        """
        name = name.upper().strip()
        cond = self.df['Denominazione'].map(
            lambda x: x.strip().rfind(name) >= 0)
        # Check if the name is founded
        df = self.df.loc[cond]
        # If found nothing
        if df.empty:
            cond_start = self.df['Denominazione'].map(
                                    lambda x: x.lstrip().startswith(name))
            df = self.df.loc[cond_start]
        # Check the status, if present
        if status is not None:
            cond_status = df['StatoImpresa'].map(
                lambda x: x.strip() in status)
            df = df.loc[cond_status]
        return df

    def find_cf(self, cf):
        """
        Metodo che dato un codice fiscale ritorna le info sull'azienda.
        """
        cf = cf.strip()
        if len(cf) < 11:
            condition = self.df['CF'].map(
                lambda x: x.lstrip().startswith(cf) >= 0)
        elif len(cf) == 11:
            condition = self.df['CF'].map(
                lambda x: x.strip().rfind(cf) >= 0)
        else:
            raise ValueError("CF non corretto.")
        return self.df.loc[condition]

if __name__ == '__main__':
    print("Prova della classe Anagrafica:")
    try:
        prova = Anagrafica()
    except ConnectionError:
        print("Connessione al DB fallita.")

