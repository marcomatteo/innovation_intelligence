import logging

from io import StringIO

class TestLogger:
    log_new_line = "-".join(["-"]*10)

    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)

