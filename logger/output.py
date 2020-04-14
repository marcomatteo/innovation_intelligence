import logging
import os
from io import StringIO

class TestOutput:
    log_new_line = "-".join(["-"]*10)
    root_dir = r"/mnt/c/Users/buzzulini/Documents/GitHub/I2FVG_scripts/"\
        + r"innovation_intelligence/logs/"

    def __init__(self, logger_name: str):
        """
        TestLogger is a class for logging while running tests
        in the innovation intelligence app
        
        Arguments:
            logger_name {str} -- Test topic to be logged
        """
        self.name = logger_name
        self.logger = logging.getLogger(logger_name)
        self.path = self.root_dir + self.name

        ch = logging.StreamHandler()   
        ch.setLevel(logging.INFO)

        ch_format = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
        ch.setFormatter(ch_format)

        self.logger.addHandler(ch)

    def add_file_handler(self, 
                         file_name: str, 
                         level = logging.DEBUG, 
                         msg_format = "%(asctime)s %(levelname)-8s %(message)s",
                         *args, **kwargs):
        """
        Add a file Handler to log messages in DEBUG (default)
        
        Arguments:
            file_name {str} -- file name to be written with extension

            level {int} -- Debug level (default)

            msg_format {str} -- Only the message (default)
        """
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        path = self.path + r"/{}".format(file_name)
        if not os.path.isfile(path):
            with open(path, 'w'):
                pass

        fh = logging.FileHandler(path, encoding="utf-8", *args, **kwargs)    
        fh.setLevel(level)

        fh_format = logging.Formatter(msg_format)
        fh.setFormatter(fh_format)

        self.logger.addHandler(fh)
