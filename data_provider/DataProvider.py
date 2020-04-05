import numpy as np
import pandas as pd

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DataProvider(metaclass = Singleton):

    def __init___(self):
        pass

if __name__ == '__main__':
    print("DataProvider.py")