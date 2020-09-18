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
    # Dispose blank line, and separate lines
    list_data = [s.split(",") for s in data.split()]
    list_dict = []
    # Map each line to dictionary
    list_dict = list([{key: (value.strip()) for key, value in zip(
        list_data[0], i)}for i in list_data[1:]])
    return list_dict
    raise NotImplementedError


def task1(filename: str):
    """
    Task 1

    @filename: the file name of the data file.

    @return: a list of flight number strings.
    """
    # Read in the data from the CSV file `filename` with tools you build in task 0.
    data = read_csv_for_data(filename)
    # Pick out the valid data
    flight_list = list(map(lambda datum: (datum["AIRLINE"], datum["FLIGHT_NUMBER"], datum["DISTANCE"]), filter(
        lambda data: int(data["DISTANCE"]) > 1500, data)))
    # Hadling the format
    flight_list.sort(key=lambda it: (int(it[2]), it[0] + it[1]))
    final_list = list(map(lambda datum: datum[0] + datum[1],
                          flight_list))
    return final_list
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
    # Try to convert string to integer
    def convert(key_):
        try:
            converted_key = int(key_)
            return converted_key
        except ValueError:
            return key_

    # Read in the data from the CSV file `filename` with tools you build in task 0.
    data = read_csv_for_data(filename)
    # Pick out selected data
    selected_data = filter(lambda airline_: airline_[
                           "AIRLINE"] == airline, data)
    # Calculate by giving key and value
    value = convert(value)
    count = 0
    for raw_datum in selected_data:
        datum = convert(raw_datum[key])
        if datum < value:
            count += 1
    return count
    raise NotImplementedError


def task3(filename: str) -> List[Tuple[str, float]]:
    """
    Task 3

    @filename: the file name of the data file.

    @return: a list of tuples with format of (airline, rate).
    """
   # Read in the data.
    data = read_csv_for_data(filename)
    # Claculate on-time rate
    airline_dict = {}
    for datum in data:
        if datum["AIRLINE"] not in airline_dict:
            airline_dict[datum["AIRLINE"]] = [0, 1]
        else:
            airline_dict[datum["AIRLINE"]][1] += 1
        if datum["ARRIVAL_DELAY"][0] == "-":
            airline_dict[datum["AIRLINE"]][0] += 1
    airline_list = list(map(lambda dicts: (
        dicts[0], dicts[1][0]/dicts[1][1]), airline_dict.items()))
    # Sort the on-time rate
    airline_list.sort(key=lambda it: it[0])
    airline_list.sort(key=lambda it: it[1], reverse=True)
    return list(airline_list)
    raise NotImplementedError


if __name__ == "__main__":
    print(task1(r"data/sample.csv"))
    pass
