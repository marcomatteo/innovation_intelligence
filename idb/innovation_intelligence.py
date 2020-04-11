# from utilities import ROOT, Singleton
import pandas as pd
from sqlalchemy import create_engine, inspect

# from utilities import Singleton

class InnovationIntelligence():
    """
    InnovationIntelligence is the interface to the
    database that stores all the informations about firms.

    It can be use a builder class for a high dimensional
    DataFrame with many configurations as are the informations 
    stored in the Innovation Intelligence DB.    
    
    """

    def __init__(self, inTest=True):
        self.inTest = inTest

    @staticmethod
    def connect(inTest=True):
        return InnovationIntelligence(inTest)