import logging
import os
from io import StringIO

class TestOutput:
    
    root_dir = r"logs/"

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

        ch = self.get_console_handler()
        self.logger.addHandler(ch)
        
    @staticmethod
    def get_console_handler(
            level = logging.INFO,
            msg_format = "%(asctime)s %(levelname)-8s %(message)s",
            *args, **kwargs) -> logging.StreamHandler:
        """
        Add a Console Handler to the Logger

        Keyword Arguments:
            level {int} -- (default: {logging.INFO})
            msg_format {str} -- (default: {"%(asctime)s %(levelname)-8s %(message)s"})

        Returns:
            logging.StreamHandler
        """
        ch = logging.StreamHandler()   
        ch.setLevel(level)

        ch_format = logging.Formatter(msg_format)
        ch.setFormatter(ch_format)

        return ch

    @staticmethod
    def get_file_handler( 
            file_path: str, 
            level = logging.DEBUG, 
            msg_format = "%(asctime)s %(levelname)-8s %(message)s",
            *args, **kwargs) -> logging.FileHandler:
        """
        Add a file Handler to log messages in DEBUG (default)
        
        Arguments:
            file_path {str} -- file name to be written with extension

            level {int} -- Debug level (default)

            msg_format {str} -- Only the message (default)
        """
        directory = file_path.rsplit('/', maxsplit=1)[0]

        if not os.path.isdir(directory):
            os.makedirs(directory)

        if not os.path.isfile(file_path):
            with open(file_path, 'w'):
                pass

        fh = logging.FileHandler(file_path, encoding="utf-8", *args, **kwargs)    
        fh.setLevel(level)

        fh_format = logging.Formatter(msg_format)
        fh.setFormatter(fh_format)

        return fh
