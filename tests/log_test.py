import unittest
import logging
import sys

import pandas as pd
import numpy as np

from io import StringIO

class LogCaptureResult(unittest.TextTestResult):

    def _exc_info_to_string(self, err, test):
        # jack into the bit that writes the tracebacks, and add captured log
        tb = super(LogCaptureResult, self)._exc_info_to_string(err, test)
        captured_log = test.stream.getvalue()
        return '\n'.join([tb, 'CAPTURED LOG', '=' * 70, captured_log])

class LogCaptureRunner(unittest.TextTestRunner):

    def _makeResult(self):
        # be nice if TextTestRunner just had a class attr for defaultResultClass
        return LogCaptureResult(self.stream, self.descriptions, self.verbosity)

class LogThisTestCase(type):

    def __new__(cls, name, bases, dct):
        # if the TestCase already provides setUp, wrap it
        if 'setUp' in dct:
            setUp = dct['setUp']
        else:
            setUp = lambda self: None
            print("creating setUp...")

        def wrappedSetUp(self):
            # for hdlr in self.logger.handlers:
            #    self.logger.removeHandler(hdlr)
            self.hdlr = logging.StreamHandler(sys.stdout)
            self.logger.addHandler(self.hdlr)
            setUp(self)
        dct['setUp'] = wrappedSetUp

        # same for tearDown
        if 'tearDown' in dct:
            tearDown = dct['tearDown']
        else:
            tearDown = lambda self: None

        def wrappedTearDown(self):
            tearDown(self)
            self.logger.removeHandler(self.hdlr)
        dct['tearDown'] = wrappedTearDown

        # return the class instance with the replaced setUp/tearDown
        return type.__new__(cls, name, bases, dct)

class BaseTestCase(unittest.TestCase):
    log_new_line = "-".join(["-"]*10)

    @staticmethod
    def logDataFrameInfo(obj):
        """

        """
        logger = logging.getLogger()
        buf = StringIO()
        obj.info(buf=buf)
        s = buf.getvalue().encode().decode('utf-8')
        logger.debug("\n\n```\n{}\n```\n".format(s))

    @staticmethod
    def logDifferences(db_info, file_info: dict):
        """

        """
        database_column_name = "Database"
        dataProvider_column_name = "DataProvider"
        logger = logging.getLogger()
        if isinstance(db_info, list):
            db_series = pd.Series(
                db_info,
                index = range(len(db_info)),
                name = database_column_name
            )
        elif isinstance(db_info, dict):
            db_series = pd.Series(
                db_info,
                name = database_column_name
            )

        file_series = pd.Series(file_info, name = dataProvider_column_name)

        df = db_series.to_frame().join(
            file_series,
            how="outer"
        )
        df.dropna(inplace=True)
        logger.debug("\n\n{}\n".format(df.to_markdown()))

    @staticmethod
    def logDifferences_types(obj, cols: dict):
        """
        Non mi ricordo
        """
        logger = logging.getLogger()
        col_list = [
            i
            for i, val in cols.items()
            if val == False
        ]
        if isinstance(obj, pd.DataFrame):
            df = obj.iloc[:, col_list]
        elif isinstance(obj, pd.Series):
            df = obj.to_frame()
        
        values = [
            str(df[col].astype('object').unique())
            for col in df.columns
        ]
        if len(col_list) == 0:
            logger.debug("\n\n**OK**\n\n")
        else:
            logger.debug("\n\n```\n{}\n```\n".format(
                "\n\n".join(values)
            )
        )
    
    @staticmethod
    def logDataFrame(df, cols=None):
        """
        Metodo per stampare un DataFrame per file markdown

        Attributes:
        -----------
            df: pandas.DataFrame

            cols: str
            Nome della singola colonna da stampare
        """
        logger = logging.getLogger()
        if cols:
            logger.debug("\n\n{}\n".format(
                df.loc[:, cols].to_markdown())
            )
        else:
            logger.debug("\n\n{}\n".format(
                df.to_markdown())
            )

    @staticmethod 
    def logObject(obj):
        """
        Log some object (list / set / np.array / pd.Series)
        """
        logger = logging.getLogger()
        logger.debug("\n\n```\n{}\n```\n".format(obj))
    
    @classmethod
    def logInfoTitle(cls, message):
        logger = logging.getLogger()
        logger.info("\n\n# {}\n{}\n".format(
            message,
            cls.log_new_line
        ))
    
    @staticmethod
    def logInfoMessage(message):
        logger = logging.getLogger()
        logger.info("\n\n{}\n".format(message))

    @staticmethod
    def logDebugMessage(message):
        logger = logging.getLogger()
        logger.debug("\n\n{}\n".format(message))
    
    @staticmethod
    def logErrorMessage(message):
        logger = logging.getLogger()
        logger.error("\n\n{}\n".format(message))

    @staticmethod
    def logTestTile(message):
        logger = logging.getLogger()
        logger.debug("\n\n### {}\n".format(message))

    def setUp(self, *args, **kwargs):
        logger = logging.getLogger()
        super().setUp(*args, **kwargs)
        # Log inizio esecuzione della funzione
        logger.debug("\n\n")
        # create a in memory stream
        self.stream = StringIO()
        # add handler to logger
        self.handler = logging.StreamHandler(self.stream)
        logger.addHandler(self.handler)

    def tearDown(self, *args, **kwargs):
        logger = logging.getLogger()
        super().tearDown(*args, **kwargs)
        # Log fine esecuzione della funzione
        logger.debug("\n\n{}".format(self.log_new_line))
        # we're done with the caputre handler
        logger.removeHandler(self.handler) 