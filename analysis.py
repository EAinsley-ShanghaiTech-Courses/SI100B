from typing import List, Tuple


def read_csv_for_data(filename: str):
    """
    Task 0

    @filename: the file name of the file you need to read in;

    @return: your custom data structure.
    """
    with open(filename) as f:
        data = f.read()
    # you may check input by uncommenting next line
    # print(data)
    raise NotImplementedError


def task1(filename: str):
    """
    Task 2

    @filename: the file name of the data file.

    @return: a list of flight number strings.
    """
    # Read in the data from the CSV file `filename` with tools you build in task 0.
    data = read_csv_for_data(filename)

    # Now write your filtering code.
    ## YOUR CODE HERE ##
    raise NotImplementedError


def task2(filename: str, airline: str, key: str, value) -> int:
    """
    Task 2

    @filename: the file name of the data file.
    @airline: the airline as a string of IATA code.
    @key: the key that we want to filter against.
    @value: the value that we want to filter against.

    @return: the number of flights that satisfy as an integer.
    """
    # Read in the data from the CSV file `filename` with tools you build in task 0.
    data = read_csv_for_data(filename)

    # Now write your filtering code.
    ## YOUR CODE HERE ##
    raise NotImplementedError


def task3(filename: str) -> List[Tuple[str, float]]:
    """
    Task 3

    @filename: the file name of the data file.

    @return: a list of tuples with format of (airline, rate).
    """
    ## YOUR CODE HERE ##
    raise NotImplementedError


if __name__ == "__main__":
    pass
