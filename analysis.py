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
        self.__data = [
            Row.__normalize_data(i, keys[data.index(i)]) for i in data
        ]
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
        with open(filename) as f:
            data = f.read()
        # read from filename
        if rows is None or keys is None:
            list_data = [[ps.strip() for ps in s.split(",")]
                         for s in data.splitlines() if s.strip() != ""]
            if list_data != []:
                self.__keys = list_data[0]
            else:
                self.__keys = []
            self.__content = [
                Row(self.__keys, datum) for datum in list_data[1:]
            ]
        else:
            self.__content = [datum for datum in rows]
            self.__keys = [key for key in keys]
        self.__keys.sort()
        self.__ids = [datum.get_id() for datum in self.__content]
        self.__filename = filename

    def __iter__(self):
        # return an iterator.
        return TableIter(self)

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

    def get_ids(self):
        return self.__ids

    def export(self, columns=None, filename=None):
        # Your code here
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
    def __init__(self, table):
        self.__table = table
        self.__ids = table.get_ids()
        self.__idx = -1

    def __next__(self):
        iter_seq = sorted(self.__ids.copy())
        self.__idx += 1
        if self.__idx >= len(self.__ids):
            raise StopIteration
        return self.__table[iter_seq[self.__idx]]


class Query:
    """
    The `Query` class.
    """
    def __init__(self, query):
        # Your code here
        self.__condition = self.__normalize_data(query["condition"])
        self.__filename = query["filename"]
        self.__table = Table(self.__filename)
        self.__keys = self.__table.keys()

    def as_table(self):
        final_table = self.__table
        for filtcons in self.__condition:
            try:
                final_table = Table(
                    self.__filename,
                    rows=filter(
                        lambda x: eval('x[filtcons["key"]] ' + filtcons[
                            "operator"] + ' filtcons["value"]'), final_table),
                    keys=self.__keys)
            except KeyError:
                raise KeyError('Wrong key in query')
        return final_table

    @staticmethod
    def __normalize_data(data):
        normed_data = []
        for datum in data:
            if datum["operator"] not in ["!=", "==", ">", ">=", "<", "<="]:
                continue
            dic = {}
            dic["key"] = datum["key"].strip()
            if dic["key"] not in [
                    "AIRLINE", "TAIL_NUMBER", "ORIGIN_AIRPORT",
                    "DESTINATION_AIRPORT"
            ]:
                dic["value"] = int(datum["value"])
            else:
                dic["value"] = datum["value"]
            dic["operator"] = datum["operator"].strip()
            normed_data.append(dic)
        return normed_data


class AggQuery(Query):
    """
    The `AggQuery` class
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
        results = []
        ids = 0
        for key, value in dic.items():
            if self.__function == "MAX":
                result = Row(keys, [key, ids, max(value)])
            elif self.__function == "AVG":
                result = Row(keys, [key, ids, sum(value) / len(value)])
            results.append(result)
            ids += 1
        return Table(self.__filename, rows=results, keys=keys)


if __name__ == "__main__":
    pass
