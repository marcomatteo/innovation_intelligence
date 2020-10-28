"""
Modulo che contiene funzioni utili per certificare efficacemente
e in modo esaustivo le US di Innovation Intelligence
"""
from datetime import datetime
import logging
import os
import pandas as pd
import warnings
import pathlib

def trim_cols(col):
    """Elimina gli spazi prima e dopo in ogni riga della colonna col"""
    warnings.warn("Use trim_columns_spaces()")
    return col.map(lambda x: str(x).strip())

def trim_columns_spaces(col):
    """Elimina gli spazi prima e dopo in ogni riga della colonna col"""
    return col.map(lambda x: str(x).strip())

def dataframe_index_differences(df1: pd.DataFrame, df2: pd.DataFrame, how='outer') -> pd.DataFrame:
    """
    Funzione che controlla se gli indici di due DataFrame
    corrispondono e sono uguali
    """
    types_join = ['inner', 'left', 'right', 'left', 'outer']
    if how not in types_join:
        raise AttributeError("Invalid type of join")

    left_index_levels = df1.index.nlevels
    right_index_levels = df2.index.nlevels

    # Check if indexes have the same shape
    if left_index_levels != right_index_levels:
        raise ValueError("DataFrames have different index shape")
    
    # Rename indici per il join
    names = ['idx_' + str(i) for i in range(left_index_levels)]
    df1.index.set_names(names, inplace = True)
    df2.index.set_names(names, inplace = True)

    df_join = df1.join(
            df2,
            how = how,
            lsuffix="_left",
            rsuffix="_right"
        )

    check = df_join.isnull().any(axis=1)

    return df_join.loc[check]

def create_logger(dp: str, path=None):
    LOG_FILE_NAME = datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    LOG_DIR = path    

    if not LOG_DIR:
        LOG_DIR = os.path.dirname(__file__) + r"/../logs/"

    LOG_DIR += r"acceptance_tests/{}/".format(dp)
    pathlib.Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    LOG_FILE = LOG_DIR + LOG_FILE_NAME

    # create logger
    logger = logging.getLogger(dp)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(LOG_FILE, mode='w')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    # ch = logging.StreamHandler(stream=sys.stdout)
    # ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-5s %(name)-8s (%(funcName)s) %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S")
    fh.setFormatter(formatter)
    # ch.setFormatter(formatter)

    # add the handlers to the logger
    # logger.addHandler(ch)
    logger.addHandler(fh)

    return logger