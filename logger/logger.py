import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)

import logging
import os
from io import StringIO

class TestLogger:
    log_new_line = "-".join(["-"]*10)
    root_dir = ROOT + r"/logs/"

    def __init__(self, logger_name, file_name):
        self.logger = logging.getLogger(logger_name)

        path_dir = self.root_dir + logger_name
        if not os.path.isdir(path_dir):
            os.mkdir(path_dir)

        path = path_dir + r"/{}".format(file_name)
        if not os.path.isfile(path):
            with open(path, 'w'):
                pass

        fh = logging.FileHandler(path, encoding="utf-8")    
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()   
        ch.setLevel(logging.INFO)

        fh_format = logging.Formatter("%(message)s")
        fh.setFormatter(fh_format)
        
        ch_format = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
        fh.setFormatter(ch_format)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


    def log_title(self, title):
        self.logger.debug("# {}\n{}\n".format(
            title,
            self.log_new_line
        ))
