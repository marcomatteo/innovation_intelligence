import logging
import pandas as pd
import numpy as np
from datetime import datetime

from io import StringIO
from logger import TestOutput

class TestMarkdown(TestOutput):

    path = TestOutput.root_dir + r"markdowns/"
    separator_line = "-".join(["-"]*10)

    def __init__(self, logger_name):
        self.logger_name = logger_name
        self.logger = self.setup_custom_logger(self.logger_name)

    @staticmethod
    def setup_custom_logger(logger_name: str) -> logging.Logger:
        file_name = datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + ".md"
        file_path = TestMarkdown.path + logger_name + r"/" + file_name

        fh = TestOutput.get_file_handler(file_path)
        ch = TestOutput.get_console_handler()
        
        logger = logging.getLogger(logger_name)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def log_title(self, title: str):
        logger = self.logger #logging.getLogger(self.logger_name)
        logger.debug("# {}\n{}\n".format(
            title,
            self.separator_line
        ))

    @staticmethod
    def log_separator_line():
        logger = logging.getLogger()
        logger.info("\n\n{}".format(TestMarkdown.separator_line))

    @staticmethod
    def log_series(s: pd.Series, message: str=None):
    
        if not isinstance(s, pd.Series):
            raise TypeError("Argument must be a pandas.Series")
        
        logger = logging.getLogger()
        logger.debug("{}\n\n{}\n".format(
            message if message else "",
            s.to_frame().to_markdown()
        ))

    @staticmethod
    def log_dataframe(df: pd.DataFrame, message: str=None):

        if not isinstance(df, pd.DataFrame):
            raise TypeError("Argument must be a pandas.DataFrame")
        
        logger = logging.getLogger()
        logger.debug("{}\n\n{}\n".format(
            message if message else "",
            df.to_markdown()))

    @staticmethod
    def log_dataframe_info(df: pd.DataFrame):
        """
        Log the StringIO buffer from pd.DataFrame.info() method
        """
        logger = logging.getLogger()
        buf = StringIO()
        df.info(buf=buf)
        stream = buf.getvalue().encode().decode('utf-8')
        logger.debug("\n\n```\n{}\n```\n".format(stream))

    @staticmethod
    def log_array(obj, message: str=None):
        """
        Log some array object into file like:
        - list
        - set
        - np.array
        
        Arguments:
            obj {list/set/np.array} -- Log this object into markdown
        """
        logger = logging.getLogger()
        cond1 = not isinstance(obj, list)
        cond2 = not isinstance(obj, set)
        cond3 = not isinstance(obj, np.ndarray)
        if cond1 and cond2 and cond3:
            raise TypeError("Argument must be list/set/np.array")

        logger.debug("{}\n\n```\n{}\n```\n".format(
                    message if message else "", obj)
                )