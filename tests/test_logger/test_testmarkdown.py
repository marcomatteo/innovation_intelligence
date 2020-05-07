import sys
ROOT = r"C:/Users/buzzulini/Documents/GitHub/I2FVG_scripts/innovation_intelligence"
if ROOT not in sys.path:
    sys.path.append(ROOT)
    
import unittest as test
from logger import TestMarkdown

class Test_TestMarkdown(test.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.name = "test_log"
        cls.log_class = TestMarkdown(cls.name)
        # cls.test_logger = TestMarkdown.setup_custom_logger(cls.name)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_log_debug_message(self):
        with self.assertLogs("test_log", level="DEBUG") as cm:
            self.log_class.logger.debug("First message")
        
        self.assertEqual(cm.output, ["DEBUG:test_log:First message"])

    def test_log_title(self):
        with self.assertLogs("test_log", level="INFO") as cm:
            self.log_class.log_title("First message")
        
        self.assertEqual(cm.output, 
                         ["INFO:test_log:# First message\n{}\n".format(
                             TestMarkdown.separator_line)]
                        )
