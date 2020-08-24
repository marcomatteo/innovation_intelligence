import unittest
from acceptance_builder import AcceptanceBuilder

class TestAcceptanceBuilderBaseClass(unittest.TestCase):
    
    maxDiff = None

    builder = NotImplemented    # type: AcceptanceBuilder
