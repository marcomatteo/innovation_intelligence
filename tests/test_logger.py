import unittest as test
import logging
from logger import TestLogger

class Test_TestLogger(test.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_logger = TestLogger("test_log", "log.md")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_log_debug_message(self):
        with self.assertLogs("test_log", level="DEBUG") as cm:
            logging.getLogger("test_log").debug("First message")
        
        self.assertEqual(cm.output, ["DEBUG:test_log:First message"])

    def test_log_title(self):
        self.assertTrue(True)
