import unittest
from io import StringIO
import os

path = r'innovation_intelligence\tests\Log'
log_file = r'test.log'

with open(os.path.join(path, log_file), 'w') as fp: 
    pass

import logging
logging.basicConfig(level=logging.DEBUG, filename=path + r'\'' + log_file, filemode='w')
logger = logging.getLogger()


class LogCaptureResult(unittest._TextTestResult):

    def _exc_info_to_string(self, err, test):
        # jack into the bit that writes the tracebacks, and add captured log
        tb = super(LogCaptureResult, self)._exc_info_to_string(err, test)
        captured_log = test.stream.getvalue()
        return '\n'.join([tb, 'CAPTURED LOG', '=' * 70, captured_log])


class LogCaptureRunner(unittest.TextTestRunner):

    def _makeResult(self):
        # be nice if TextTestRunner just had a class attr for defaultResultClass
        return LogCaptureResult(self.stream, self.descriptions, self.verbosity)


class BaseTestCase(unittest.TestCase):

    def setUp(self, *args, **kwargs):
        super(BaseTestCase, self).setUp(*args, **kwargs)
        # create a in memory stream
        self.stream = StringIO()
        # add handler to logger
        self.handler = logging.StreamHandler(self.stream)
        logger.addHandler(self.handler)

    def tearDown(self, *args, **kwargs):
        super(BaseTestCase, self).tearDown(*args, **kwargs)
        # we're done with the caputre handler
        logger.removeHandler(self.handler)


class MyTestCase(BaseTestCase):

    def test_something(self):
        logger.debug('testing something')
        self.assert_(True)
        logger.debug('everything worked, no need to see logs')

    def test_something_broken(self):
        logger.debug('seeing if this broke thing works')
        try:
            raise Exception('kaboom!')
        except:
            logger.debug('hrmm... that did not go well')
            self.assert_(False)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(MyTestCase)
    runner = LogCaptureRunner(verbosity=2)
    runner.run(suite)