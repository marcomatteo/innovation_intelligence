from file_parser import ParserXls
from data_provider import DataProvider

import pandas as pd
import numpy as np


class ContrattiRete(DataProvider):

    def __init__(self, inTest=False):
        """
        ContrattiRete data provider

        Keyword Arguments:
            inTest {bool} -- opening test file (default: {False})
            preprocessed {bool} -- appending "Sogg. Giu." sheet
                into the "Elenco" DataFrame (default: {True})
        """
        self.inTest = inTest
        self.file_path = self.root_path + r"ContrattiRete/"
        self.file_parser = ParserXls(
            self.file_path + "ContrattiReteSourceSample.xlsx")

        self.column_types = {
            0: 'int',
            1: 'object',
            2: 'date',
            3: 'object',
            4: 'object',
            5: 'object',
            6: 'object',
            7: 'object',
            8: 'object',
            9: 'object',
            10: 'object',
            11: 'object',
            12: 'object',
            13: 'object',
            14: 'object',
            15: 'object',
            16: 'object',
            17: 'object',
            18: 'object'
        }
        self.column_constraints = {
            i: False for i in range(len(self.column_types))}
        self.column_constraints[3] = True
        self.column_constraints[4] = True
        self.column_constraints[7] = True

        self.unique_column_names = [
            'numero repertorio', 'numero atto', 'c.f.']

        self.open_dataframe_from_sheet_name(sheet_name="NuovoElenco")

    def open_dataframe_from_sheet_name(self, sheet_name):
        try:
            df = self.file_parser.open_file(sheet_name=sheet_name)
        except:
            print("Il file dev'essere elaborato. Dopo l'elaborazione, ricordati di eseguire i passaggi:\
                \n\t1. rinominare il foglio 'Elenco' in 'VecchioElenco'\
                \n\t2. rinominare il foglio 'NuovoElenco' in 'Elenco'\n")
            self.preprocessing()
        else:
            self.df = df

    def preprocessing(self):
        """
        Elaborazioni:

            1. Accodamento contratti di rete presenti nel foglio "Sogg. Giu."
                nel dataframe self.df

            2. Salvataggio dei DataFrame nel file
        """
        self.old_df = self.file_parser.open_file(sheet_name="Elenco")
        self.df = self.old_df.astype({'progr.': np.int64})
        self.df_to_append = self.file_parser.open_file(
            sheet_name="Sogg. Giu.").astype({'progr.': np.int64})

        print("Accodamento contratti che sono soggetto giuridico...")
        self.append_dataframe()

        print("Selezione dei soli codici fiscali presenti in I2FVG...")
        self.set_filtred_fiscal_codes_dataframe()

        if not self.is_valid_data_provider():
            self.update_duplicates_sheet()

        self.update_preprocessed_sheet()

    def append_dataframe(self):
        """
        Method that append the self.df_to_append to self.df
        """
        self.updated_columns_from_sheets()

        self.align_df_to_append()

        self.df = self.df.append(
            self.df_to_append, ignore_index=True, sort=False)

    def updated_columns_from_sheets(self):
        """
        Method that update the columns for each DataFrame
        """
        step = self.df['progr.'].max()
        self.df_to_append.loc[:, 'progr.'] += step

        new_column_name = "SoggettoGiuridico"
        self.df[new_column_name] = "NO"
        self.df_to_append[new_column_name] = "SI"

    def align_df_to_append(self):
        """
        Align the self.df_to_append
        """
        mapping_dict = self.get_mapped_columns_from_sheets()

        column_selection = [
            column for column in mapping_dict.values() if len(column) > 1]

        self.df_to_append = self.df_to_append.rename(
            columns=mapping_dict).loc[:, column_selection]

    def get_mapped_columns_from_sheets(self) -> dict:
        """
        Return the mapping dictionary between the two dataframes
        """
        elenco_cols1 = self.df.columns.tolist()
        elenco_cols2 = self.df_to_append.columns.tolist()
        cols = {col: col[0] for col in elenco_cols2}

        # Match chiave e valori del dizionario per rinominare le colonne
        cols[elenco_cols2[0]] = elenco_cols1[0]
        cols[elenco_cols2[1]] = elenco_cols1[1]
        cols[elenco_cols2[4]] = elenco_cols1[2]
        cols[elenco_cols2[9]] = elenco_cols1[3]
        cols[elenco_cols2[10]] = elenco_cols1[5]
        cols[elenco_cols2[12]] = elenco_cols1[6]
        cols[elenco_cols2[13]] = elenco_cols1[7]
        cols[elenco_cols2[14]] = elenco_cols1[8]
        cols[elenco_cols2[15]] = elenco_cols1[10]
        cols[elenco_cols2[16]] = elenco_cols1[11]
        cols[elenco_cols2[17]] = elenco_cols1[12]
        cols[elenco_cols2[18]] = elenco_cols1[13]
        cols[elenco_cols2[19]] = elenco_cols1[14]
        cols[elenco_cols2[20]] = elenco_cols1[18]

        return cols

    def set_filtred_fiscal_codes_dataframe(self) -> None:
        """
        Overright del metodo DataProvider per selezionare solo
        i Contratti di Rete che hanno aziende di Innovation Intelligence

        Arguments:
            cf_column {int} -- Numero della colonna del C.F.
        """
        selected_dataframe = self.get_filtred_fiscal_codes_dataframe(
            cf_column=7)

        selection_filter = self.get_contratti_filter(selected_dataframe)

        self.df = self.df.loc[selection_filter].reset_index()
        self.df.drop(columns='index', inplace=True)

    def get_contratti_filter(self, selected_dataframe: pd.DataFrame) -> pd.Series:
        """
        [summary]

        Returns:
            pd.Series -- [description]
        """
        numero_repertorio_list = selected_dataframe["numero repertorio"] \
            .drop_duplicates().tolist()
        numero_atto_list = selected_dataframe["numero atto"] \
            .drop_duplicates().tolist()

        numero_repertorio_filter = self.df["numero repertorio"].isin(
            numero_repertorio_list)
        numero_atto_filter = self.df["numero atto"].isin(numero_atto_list)

        return numero_repertorio_filter & numero_atto_filter

    def is_valid_data_provider(self) -> bool:
        """
        Check if duplicates founded and return True else return False 
        """
        df_duplicates = self.get_duplicates_dataframe()

        return df_duplicates.empty

    def update_duplicates_sheet(self):
        """
        Save the duplicati sheet
        """
        duplicates = self.get_duplicates_dataframe()
        # Memory for drop rows after the cleaning
        duplicates["indice"] = duplicates.index

        print("Sono stati trovati duplicati. Tutti i duplicati sono salvati nel foglio 'Duplicati'")
        self.write_new_dataframe_into_file_parser(duplicates,
                                                  sheet_name="Duplicati")

        print(f"Trovati n. {duplicates.shape[0]} duplicati da ripulire manualmente " +
              "contrassegnando i contratti non validi da dover eliminare")

    def get_duplicates_dataframe(self) -> pd.DataFrame:
        """
        Return pandas.DataFrame of duplicates values

        Returns:
            pd.DataFrame -- copy of the original DataFrame only with duplicates
        """
        is_duplicate_filter = self.get_duplicates_bool_series()
        return self.df.loc[is_duplicate_filter].copy()

    def get_duplicates_bool_series(self) -> pd.Series:
        """
        Return the boolean series for duplicate selection

        Returns:
            pd.Series -- [description]
        """
        return self.df.duplicated(subset=self.unique_column_names,
                                  keep=False)

    def write_new_dataframe_into_file_parser(self,
                                             df: pd.DataFrame,
                                             sheet_name: str):
        """
        Write into the Parser
        """
        try:
            self.file_parser.write_new_sheet_into_file(df,
                                                       sheet_name=sheet_name)
        except:
            print("Cannot write the new sheet into the same file! \
                    \nHint: save the file in xlsx format")

    def update_preprocessed_sheet(self):
        """
        Update the file_parser saving the old sheet into "ElencoOld" and
        sostitute the "Elenco" file with the preprocessed DataFrame
        """
        print("Salvataggio nel foglio 'NuovoElenco' dei contratti di rete\n" +
              "Ricordati di rinominare i fogli prima di consegnare il file")
        self.write_new_dataframe_into_file_parser(self.df,
                                                  sheet_name="NuovoElenco")
