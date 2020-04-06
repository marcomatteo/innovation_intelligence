import abc
import pandas as pd

class IParser(metaclass = abc.ABCMeta):
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "open_file") and 
                callable(subclass.open_file) or
                NotImplemented)
    
    @abc.abstractmethod
    def open_file(self) -> pd.DataFrame:
        """Load the data as a pandas.DataFrame"""
        raise NotImplementedError
    
    @staticmethod
    def get_file_ext(file_name):
        """
        Return the file_name extension after the '.'
        """
        return file_name.split(".")[-1]

if __name__ == '__main__':
    print("IParser.py")
    