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
    def logInfo(obj):
        logger = logging.getLogger()
        buf = StringIO()
        obj.info(buf=buf)
        s = buf.getvalue().encode().decode('utf-8')
        logger.debug("\n```\n{}\n```\n".format(s))

    @staticmethod
    def logDifferences(db_info, file_info: dict):
        logger = logging.getLogger()
        if isinstance(db_info, list):
            db_series = pd.Series(
                db_info,
                index=range(len(db_info)),
                name="DB"
            )
        elif isinstance(db_info, dict):
            db_series = pd.Series(
                db_info,
                name="DB"
            )

        file_series = pd.Series(file_info, name="DP")

        df = db_series.to_frame().join(
            file_series,
            how="outer"
        )
        df.dropna(inplace=True)
        logger.debug("\n{}\n".format(df.to_markdown()))

    @staticmethod
    def logDifferences_types(obj, cols: dict):
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
            logger.debug("\n```\n{}\n```\n".format(
                "\n\n".join(values)
            )
        )

    