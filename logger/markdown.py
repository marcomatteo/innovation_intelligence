import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)

import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime

from io import StringIO
from logger import TestOutput

class TestMarkdown(TestOutput):
    separator_line = "-".join(["-"]*10)

    def __init__(self, logger_name: str):
        """
        TestMarkdown is a class for logging markdown documents
        while running tests in the innovation intelligence app
        
        Arguments:
            logger_name {str} -- Test topic to be logged
        """
        self.root_dir = super().root_dir + r"/markdowns/"
        super().__init__(logger_name)
        self.add_file_handler()

    def add_file_handler(self, 
                         level = logging.DEBUG, 
                         msg_format = "%(asctime)s %(levelname)-8s %(message)s",
                         *args, **kwargs):
        """
        Add a file Handler to log a markdown file 
        for formatted output messages
        
        Arguments:

            level {int} -- Debug level (default)

            msg_format {str} -- Only the message (default)
        """
        file_name = datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + ".md"
        super().add_file_handler(file_name, level=level, msg_format="%(message)s")

    def log_title(self, title: str):
        self.logger.debug("# {}\n{}\n".format(
            title,
            self.separator_line
        ))

    def log_separator_line(self):
        self.logger.info("\n\n{}".format(self.separator_line))

    def log_series(self, s: pd.Series, message: str=None):
        if not isinstance(s, pd.Series):
            raise TypeError("Argument must be a pandas.Series")
        
        self.logger.debug("{}\n\n{}\n".format(
            message if message else "",
            s.to_frame().to_markdown()
        ))

    def log_dataframe(self, df: pd.DataFrame, message: str=None):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Argument must be a pandas.DataFrame")
        
        self.logger.debug("{}\n\n{}\n".format(
            message if message else "",
            df.to_markdown()))

    def log_dataframe_info(self, df: pd.DataFrame):
        """
        Log the StringIO buffer from pd.DataFrame.info() method
        """
        buf = StringIO()
        df.info(buf=buf)
        stream = buf.getvalue().encode().decode('utf-8')
        self.logger.debug("\n\n```\n{}\n```\n".format(stream))

    def log_array(self, obj, message: str=None):
        """
        Log some array object into file like:
        - list
        - set
        - np.array
        
        Arguments:
            obj {list/set/np.array} -- Log this object into markdown
        """
        cond1 = not isinstance(obj, list)
        cond2 = not isinstance(obj, set)
        cond3 = not isinstance(obj, np.ndarray)
        if cond1 and cond2 and cond3:
            raise TypeError("Argument must be list/set/np.array")

        self.logger.debug("{}\n\n```\n{}\n```\n".format(
            message if message else "",
            obj))