import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime

from io import StringIO
from logger import TestOutput

class TestLogger(TestOutput):

    def __init__(self, logger_name: str):
        """
        TestLogger is a class for logging while tests
        in innovation intelligence app
        
        Arguments:
            logger_name {str} -- Test topic to be logged
        """
        self.root_dir = super().root_dir + r"/txt/"
        super().__init__(logger_name)
        self.add_file_handler()

    def add_file_handler(self, 
                         level = logging.DEBUG, 
                         msg_format = "%(asctime)s %(levelname)-8s %(message)s",
                         *args, **kwargs):
        """
        Add a file Handler to log messages in DEBUG (default)
        
        Arguments:

            level {int} -- Debug level (default)

            msg_format {str} -- Only the message (default)
        """
        file_name = datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
        super().add_file_handler(file_name, level=level, msg_format="%(message)s")