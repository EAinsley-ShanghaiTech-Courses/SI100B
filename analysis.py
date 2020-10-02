# =============================================================================#
#                   Homework 2: Flight Analytics with SQL                     #
#                            Reference Solution                               #
#       SI 100B: Introduction to Information Science and Technology B         #
#                      Fall 2020, ShanghaiTech University                     #
#             Author: Wu Daqian <wudq1>, Diao Zihao <hi@ericdiao.com>         #
#                         Last motified: 09/06/2020                           #
# =============================================================================#


class Error(Exception):
    """Base class for other exceptions"""
    pass


class Row:
    """
    The `Row` class.

    You are building the row class here.
    """

    def __init__(self, keys, data):
        if not isinstance(keys, list) or not isinstance(data, list):
            raise TypeError('`data` and `key` must be list.')
        if len(data) != len(keys):
            raise KeyError('Length of `data` and `keys` are not consistent.')
        if len(data) == 0:
            raise ValueError('Empty row.')

        self.__keys = keys
        self.__data = [Row.__normalize_data(i, keys[data.index(i)]) for i in data]
        self.__id = self.__data[self.__keys.index('ID')]
        self.__sort_key()

    def __getitem__(self, key):
        try:
            idx = self.__keys.index(key)
        except ValueError:
            raise KeyError('Key `{}` is not in this row'.format(key))
        return self.__data[idx]

    def __setitem__(self, key, value):
        try:
            idx = self.__keys.index(key)
        except ValueError:
            raise KeyError('Key `{}` is not in this row'.format(key))
        self.__data[idx] = Row.__normalize_data(value, key)

    def __len__(self):
        return len(self.__keys)

    def __lt__(self, other):
        if (not isinstance(other, Row)) or self.__keys != other.__keys:
            raise TypeError

        return self.__getitem__('ID') < other.__getitem__("ID")

    def keys(self):
        return self.__keys.copy()

    def get_id(self):
        return self.__id

    def __iter__(self):
        return RowIter(self)

    def __sort_key(self):
        orig_key = self.__keys
        orig_data = self.__data
        self.__keys = sorted(self.__keys)
        self.__data = [orig_data[orig_key.index(idx)] for idx in self.__keys]

    @staticmethod
    def __normalize_data(data, key):
        if key not in ["AIRLINE", "TAIL_NUMBER", "ORIGIN_AIRPORT", "DESTINATION_AIRPORT"]:
            return int(data)
        return data


class RowIter:

    def __init__(self, row):
        self.row = row
        self.idx = -1

    def __next__(self):
        self.idx += 1
        if self.idx >= len(self.row.keys()):
            raise StopIteration
        return self.row.keys()[self.idx]


class Table:
    """
    The `Table` class.

    This class represents a table in your database. The table consists
    of one or more lines of rows. Your job is to read the content of the table
    from a CSV file and add the support of iterator to the table. See the
    specification in README.md for detailed information.
    """

    def __init__(self, filename, rows=None, keys=None):
        # Your code here
        pass

    def __iter__(self):
        # Your code here
        pass

    def __next__(self):
        # Your code here
        pass

    def __getitem__(self, key):
        # Your code here
        pass

    def __len__(self):
        # Your code here
        pass

    def keys(self):
        # Your code here
        pass

    def get_table_name(self):
        # Your code here
        pass

    def export(self, columns=None, filename=None):
        # Your code here
        pass


class Query:
    """
    The `Query` class.
    """

    def __init__(self, query):
        # Your code here
        pass

    def as_table(self):
        # Your code here
        pass

    """ 
    possible helpful function definition
    def _do_filter(self, cols, table, conds):
        # Your code here
        pass

    @staticmethod
    def __do_cmp(row, key, var, op):
        # Your code here
        pass

    @staticmethod
    def __normalize_data(data):
        # Your code here
        pass"""


class AggQuery(Query):
    """
    The `AggQuery` class
    """

    def __init__(self, query):
        # Your code here
        pass

    def as_table(self):
        # Your code here
        pass
