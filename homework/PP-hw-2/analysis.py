# =============================================================================#
#                   Homework 2: Flight Analytics with SQL                     #
#                            Reference Solution                               #
#       SI 100B: Introduction to Information Science and Technology B         #
#                      Fall 2020, ShanghaiTech University                     #
#             Author: Wu Daqian <wudq1>, Diao Zihao <hi@ericdiao.com>         #
#                         Last motified: 09/06/2020                           #
# =============================================================================#

import re


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
        self.__data = {
            k: Row.__normalize_data(d, k)
            for d, k in zip(data, keys)
        }
        self.__id = self.__data['ID']
        self.__sort_key()

    def __getitem__(self, key):
        try:
            return self.__data[key]
        except KeyError:
            raise KeyError('Key `{}` is not in this row'.format(key))

    def __setitem__(self, key, value):
        if key not in self.__data:
            raise KeyError('Key `{}` is not in this row'.format(key))
        else:
            self.__data[key] = Row.__normalize_data(value, key)

    def __len__(self):
        return len(self.__keys)

    def __lt__(self, other):
        if (not isinstance(other, Row)) or self.__keys != other.__keys:
            raise TypeError

        return self.get_id() < other.get_id()

    def keys(self):
        return self.__keys.copy()

    def get_id(self):
        return self.__id

    def __iter__(self):
        return RowIter(self)

    def __sort_key(self):
        self.__keys = sorted(self.__keys)

    @staticmethod
    def __normalize_data(data, key):
        if key not in [
                "AIRLINE", "TAIL_NUMBER", "ORIGIN_AIRPORT",
                "DESTINATION_AIRPORT"
        ]:
            if re.search('AVG\\([a-z_A-Z]+\\)', key):
                return float(data)
            return int(data)
        return data


class RowIter:
    def __init__(self, row):
        self.row = row
        self.idx = -1

    def __next__(self):
        self.idx += 1
        if self.idx >= len(self.row):
            raise StopIteration
        return self.row.keys()[self.idx]


class Table:
    """The `Table` class.

    This class represents a table in your database. The table consists
    of one or more lines of rows. `filename` must be given to specify the file
    to read in. Build from given `rows` and `keys` if neither of two is `None`.
    """
    def __init__(self, filename, rows=None, keys=None):
        # read from filename
        if rows is None or keys is None:
            with open(filename) as f:
                data = f.readlines()
            list_data = [[ps.strip() for ps in s.split(",")] for s in data
                         if s.strip() != ""]
            data = None
            if list_data:
                self.__keys = list_data[0]
                self.__content = [
                    Row(self.__keys, datum) for datum in list_data[1:]
                ]
            else:
                self.__keys = []
                self.__content = []
        # read from rows and keys
        else:
            self.__content = list(rows)
            self.__keys = keys
        self.__keys.sort()
        self.__ids = [datum.get_id() for datum in self.__content]
        self.__filename = filename

    def __iter__(self):
        # return TableIter.
        return TableIter(self, self.__ids)

    def __getitem__(self, key):
        # return row object instance
        datum_idx = self.__ids.index(key)
        if datum_idx > -1:
            return self.__content[datum_idx]
        else:
            raise ValueError('Does not contains id: {}'.format(key))

    def __len__(self):
        # return the number of rows
        return len(self.__content)

    def keys(self):
        # return the keys in the Table()
        return self.__keys.copy()

    def get_table_name(self):
        # return the table name of the table
        return self.__filename

    def export(self, columns=None, filename=None):
        """Export the Table to a file in terms of csv, sorted by ID.

        Export to given file by `filename`. Export to original file of Table if
        `filename` is None.
        Export selected columns by `columns`. Export all columns if `columns`
        is None.

        Args:
            columns: A list of string, representing the selected columns need
                to be exported.
            finename: A string represents the target file, in which to export
                the Table.
        """
        if not filename:
            filename = self.__filename
        if not columns:
            columns = self.__keys
        else:
            columns.sort()
        with open(filename, "w") as f:
            f.write(",".join([str(col) for col in columns]) + "\n")
            for rows in self:
                selected_data = [str(rows[key]) for key in columns]
                f.write(",".join(selected_data) + "\n")


class TableIter:
    def __init__(self, table, ids):
        self.__table = table
        self.__ids = sorted(ids)
        self.__index = -1

    def __next__(self):
        self.__index += 1
        if self.__index >= len(self.__ids):
            raise StopIteration
        return self.__table[self.__ids[self.__index]]


class Query:
    """The `Query` class.

    Covert the query to a table which statisfy the condition in query.
    Raise KeyError if the column requred by query not in the table.
    """
    def __init__(self, query):
        # Your code here
        self.__condition = query["condition"]
        self.__filename = query["filename"]
        self.__table = Table(self.__filename)
        self.__keys = self.__table.keys()

    def as_table(self):
        final_table = self.__table
        for filtcons in self.__condition:
            if filtcons["key"] not in [
                    "AIRLINE", "TAIL_NUMBER", "ORIGIN_AIRPORT",
                    "DESTINATION_AIRPORT"
            ]:
                filtcons["value"] = int(filtcons["value"])
            final_table = Table(
                self.__filename,
                rows=filter(
                    lambda x: eval('x[filtcons["key"]] ' + filtcons["operator"]
                                   + ' filtcons["value"]'), final_table),
                keys=self.__keys)
        return final_table


class AggQuery(Query):
    """The `AggQuery` class

    Convert an augemented query to Table.
    """
    def __init__(self, query):
        # Your code here
        self.__table = Query(query).as_table()
        self.__column = query["column"]
        self.__function = query["function"]
        self.__group_by = query["group_by"]
        self.__filename = query["filename"]

    def as_table(self):
        dic = {}
        for cols in self.__table:
            if cols[self.__group_by] in dic:
                dic[cols[self.__group_by]].append(cols[self.__column])
            else:
                dic[cols[self.__group_by]] = [cols[self.__column]]

        keys = [
            self.__group_by, "ID", "{}({})".format(self.__function,
                                                   self.__column)
        ]
        if self.__function == "MAX":
            results = [
                Row(keys, [key, ids, max(value)])
                for (ids, (key, value)) in enumerate(dic.items())
            ]
        elif self.__function == "AVG":
            results = [
                Row(keys, [key, ids, sum(value) / len(value)])
                for (ids, (key, value)) in enumerate(dic.items())
            ]
        else:
            raise ValueError("Unkown function")
        return Table(self.__filename, rows=results, keys=keys)


if __name__ == "__main__":
    print(Table(filename="data/sample.csv").export(filename="test1.csv"))
    pass