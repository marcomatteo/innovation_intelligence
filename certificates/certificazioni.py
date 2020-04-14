import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from data_provider import DataProvider

class CertificazioniMeta(type):
    def __call__(cls, *args, **kwargs):
        class_object = type.__call__(cls, *args, **kwargs)
        class_object.check_required_attributes()
        return class_object

class Certificazioni(metaclass = CertificazioniMeta):
    """
    Super classe che implementa tutte le funzioni
    da utilizzare per controllare un file fonte
    da un Data Provider
    """
    dp = NotImplemented             # type: DataProvider
    
    def check_required_attributes(self):
        if self.dp is NotImplemented:
            raise NotImplementedError("Subclass must define self.dp attribute. \n"\
                + "This attribute should define the DataProvider obj of the certificate.")
    
    def check_file_extension(self):
        if not self.dp is NotImplemented:
            return self.dp.file_parser.file_ext

    def check_column_number(self):
        if not self.dp is NotImplemented:
            return len(self.dp.get_column_names())

    def check_column_types(self):
        if not self.dp is NotImplemented:
            return self.dp.get_column_types()
        pass

    def check_column_length(self):
        if not self.dp is NotImplemented:
            return 0
        pass

    def check_column_nullables(self):
        if not self.dp is NotImplemented:
            return 0
        pass

    def check_column_constrains(self):
        if not self.dp is NotImplemented:
            return 0
        pass
    