from acceptance_builder.accredia_builder import AccrediaBuilder
from tests import TestAcceptanceBuilderBaseClass

class TestAccrediaBuilder(TestAcceptanceBuilderBaseClass):
    
    @classmethod
    def setUpClass(cls):
        cls.builder = AccrediaBuilder()

if __name__ == '__main__':
    from unittest import main
    main(verbosity=2)