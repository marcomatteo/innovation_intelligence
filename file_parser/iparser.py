import abc
import pandas as pd

class IParser(metaclass = abc.ABCMeta):
    file_path = NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "open_file") and 
                callable(subclass.open_file) or
                NotImplemented)

    @abc.abstractmethod
    def open_file(self) -> pd.DataFrame:
        """Load the data as a pandas.DataFrame"""
        raise NotImplementedError

    @property
    def file_ext(self):
        """
        Return the file_name extension after the '.'
        """
        if not self.file_path is NotImplemented:
            return self.file_path.split(".")[-1]

if __name__ == '__main__':
    print("IParser.py")
    