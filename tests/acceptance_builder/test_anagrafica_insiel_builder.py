from tests.acceptance_builder import TestAcceptanceBuilderBaseClass
from acceptance_builder import AnagraficaInsielBuilder

class TestAnagraficaInsielAcceptanceBuilder(TestAcceptanceBuilderBaseClass):

    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = AnagraficaInsielBuilder(inTest=True)
        cls.columns_length = 49

if __name__ == "__main__":
    from unittest import main
    main(verbosity=2)
