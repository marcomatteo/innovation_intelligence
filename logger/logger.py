import logging

from datetime import datetime
from logger import TestOutput

class TestLogger(TestOutput):

    path = TestOutput.root_dir + r"txt/"

    @staticmethod
    def setup_custom_logger(logger_name: str) -> logging.Logger:
        file_name = datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
        file_path = TestLogger.path + logger_name + r"/" + file_name

        fh = TestOutput.get_file_handler(file_path)
        ch = TestOutput.get_console_handler()
        
        logger = logging.getLogger(logger_name)
        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger