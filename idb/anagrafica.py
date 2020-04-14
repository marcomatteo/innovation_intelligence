import pandas as pd
import numpy as np

from idb import DatabaseConnector

class Anagrafica(DatabaseConnector):

    def __init__(self, inTest = True):
        super().__init__(inTest=inTest)
        pass