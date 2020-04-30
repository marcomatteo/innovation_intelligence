import unittest
from idb import InnovationIntelligence

class Test_InnovationIntelligence(unittest.TestCase):
    
    def test_connect_return_DataFrame(self):
        import pandas as pd        
    
        self.assertEqual(
            pd.DataFrame,
            type(InnovationIntelligence.connect().df)
        )