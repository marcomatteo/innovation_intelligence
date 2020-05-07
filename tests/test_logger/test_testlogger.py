import unittest as test
from logger import TestLogger

class Test_TestLogger(test.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_logger = TestLogger.setup_custom_logger("test_log")

    def test_log_message(self):
        with self.assertLogs("test_log", level="DEBUG") as cm:
            self.test_logger.debug("First message")
            self.test_logger.info("Info message")
        
        self.assertEqual(cm.output, ["DEBUG:test_log:First message",
                                     "INFO:test_log:Info message"])
