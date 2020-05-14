from file_parser import ParserXls
from data_provider import DataProvider

import pandas as pd


class BrevettiIta(DataProvider):

    def __init__(self, inTest=False):
        self.inTest = inTest
        self.file_path = self.root_path + r"UIBM/"
        self.file_parser = ParserXls(self.file_path + "UIBMSourceSample.xlsx")
        self.df = self.get_dataframe_merged()
        self.column_types = {
            0: 'int',
            1: 'object',
            2: 'date',
            3: 'object',
            4: 'object',
            5: 'int',
            6: 'object',
            7: 'object',
            8: 'object',
            9: 'object',
            10: 'object',
            11: 'object',
            12: 'object',
            13: 'object',
            14: 'object',
            15: 'bool'
        }
        self.column_constraints = {
            i: False for i in range(16)
        }

    def get_dataframe_merged(self) -> pd.DataFrame:
        """
        Metodo che apre tutti i fogli del file excel e li ritorna in un unico DataFrame
        """
        df_to_concat = []
        for sheet in self.file_parser.get_sheet_names:
            df_temp = self.file_parser.open_file(sheet_name=sheet)
            #df_temp["Sheet"] = sheet
            df_to_concat.append(df_temp)

        return pd.concat(df_to_concat, ignore_index=True, verify_integrity=True)
