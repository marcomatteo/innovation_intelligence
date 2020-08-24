from collections import namedtuple
from typing import List
from data_provider import DataProvider


class AcceptanceMeta(type):
    def __call__(cls, *args, **kwargs):
        class_object = type.__call__(cls, *args, **kwargs)
        class_object.check_required_attributes()
        return class_object


class AcceptanceBuilder(metaclass=AcceptanceMeta):
    """
    Super classe che implementa tutte le funzioni
    da utilizzare per controllare un file fonte
    da un Data Provider
    """
    # Soluzione alternativa ai dizionari
    Columns = namedtuple('Columns', ['nome', 'tipologia', 'lunghezza', 'nullable', 'pk'])

    dp = NotImplemented                 # type: DataProvider
    dp_file_extension = NotImplemented  # type: str
    column_number = NotImplemented      # type: int
    columns = NotImplemented            # type: List[Columns]
    
    column_types = NotImplemented       # type: list
    column_max_length = NotImplemented  # type: list
    column_nullables = NotImplemented   # type: list


    def __init__(self, dp, dp_file_extension, columns):
        self.dp = dp
        self.dp_file_extension = dp_file_extension
        self.columns = columns

    @staticmethod
    def get_log_list_from_list(elements: list) -> list:
        """
        Method to format list for logging purposes

        Arguments:
            elements {list} -- list to be printed into a logger

        Returns:
            list
        """
        result = [f"{num} : {value}" for num, value in enumerate(elements)]
        result.append("\n")

        return result

    @staticmethod
    def get_log_list_from_dict(elements: dict) -> list:
        """
        Method to format dict for logging purposes

        Arguments:
            elements {dict} -- dict to be printed into a logger

        Returns:
            list
        """
        result = [f"{num} : {value}" for num, value in elements.items()]
        result.append("\n")

        return result

    def check_required_attributes(self):
        if self.dp is NotImplemented:
            raise NotImplementedError("Subclass must define self.dp attribute. \n"
                                      + "This attribute should define the DataProvider obj of the certificate.")
        if self.dp_file_extension is NotImplemented:
            raise NotImplementedError("Subclass must define self.dp_file_extension attribute. \n"
                                      + "This attribute should define the DataProvider obj of the certificate.")
        if self.columns is NotImplemented:
            raise NotImplementedError("Subclass must define self.columns attribute. \n"
                                      + "This attribute should define the DataProvider obj of the certificate.")
        pass

    def check_file_extension(self) -> str:
        if not self.dp is NotImplemented:
            return self.dp.file_parser.file_ext
        pass

    def check_column_number(self) -> int:
        if ((not self.dp is NotImplemented) and
                (not self.columns is NotImplemented)):
            return self.dp.get_column_number()

    def check_column_types(self) -> list:
        if ((not self.dp is NotImplemented) and
                (not self.columns is NotImplemented)):
            # self.column_types = [col.tipologia for col in self.columns]
            return self.dp.get_column_types()
        pass

    def check_column_length(self) -> list:
        if ((not self.dp is NotImplemented) and
                (not self.columns is NotImplemented)):
            # self.column_max_length = [col.lunghezza for col in self.columns]
            return self.dp.get_columns_max_length()
        pass

    def check_column_nullables(self) -> list:
        if ((not self.dp is NotImplemented) and
                (not self.columns is NotImplemented)):
            # self.column_nullables = [col.nullable for col in self.columns]
            return self.dp.get_column_nullables()
        pass

    def check_column_constraints(self) -> int:
        if ((not self.dp is NotImplemented) and
                (not self.columns is NotImplemented)):
            return self.dp.get_column_constraints_is_respected().sum()
        pass
