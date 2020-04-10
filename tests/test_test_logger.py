import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)
    
import unittest as test
from logger import TestLogger

class Test_TestLogger(test.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_logger = TestLogger("test_log")
        cls.test_logger.add_file_handler()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_log_debug_message(self):
        with self.assertLogs("test_log", level="DEBUG") as cm:
            self.test_logger.logger.debug("First message")
        
        self.assertEqual(cm.output, ["DEBUG:test_log:First message"])
