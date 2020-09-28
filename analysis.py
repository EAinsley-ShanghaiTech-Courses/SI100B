from typing import List, Tuple


def read_csv_for_data(filename: str):
    """read and pre-process the data

    Args:
        filename: the file name of the file need to be read in.

    Returns:
        A list of dictionaries whose keys and values correspond to the field
        name and field content respectively.
    """
    with open(filename) as f:
        data = f.read()
    list_data = [s.split(",") for s in data.split()]
    # Map each line to dictionary
    list_dict = list([{key: (value.strip()) for key, value in zip(
        list_data[0], i)} for i in list_data[1:]])
    return list_dict


def task1(filename: str):
    """Task 1

    Args:
        filename: the file name of the data file.

    Returns:
        A list of flight number strings.
    """
    data = read_csv_for_data(filename)
    # Pick out the valid data
    flight_list = [(x["AIRLINE"]+x["FLIGHT_NUMBER"], x["DISTANCE"]) for x in filter(
        lambda data: int(data["DISTANCE"]) > 1500, data)]
    # Handling the format
    flight_list.sort(key=lambda it: (int(it[1]), it[0]))
    final_list = [x[0] for x in flight_list]
    return final_list


def task2(filename: str, airline: str, key: str, value) -> int:
    """Task 2

    Args:
        filename: the file name of the data file.
        airline: the airline as a string of IATA code.
        key: the key that we want to filter against.
        value: the value that we want to filter against.

    Returns:
        The number of flights that satisfy as an integer.
    """
    # Try to convert string to integer
    def convert(key_):
        try:
            converted_key = int(key_)
            return converted_key
        except ValueError:
            return key_

    data = read_csv_for_data(filename)
    # Pick out selected data
    selected_data = filter(lambda airline_: airline_[
                           "AIRLINE"] == airline, data)
    # Calculate by giving key and value
    value = convert(value)
    count = sum(convert(datum[key]) < value for datum in selected_data)
    return count


def task3(filename: str) -> List[Tuple[str, float]]:
    """Task 3
    Args:
        filename: the file name of the data file.

    Returns:
        A list of tuples with format of (airline, rate).
    """
    data = read_csv_for_data(filename)
    # Claculate on-time rate
    airline_dict = {}
    for datum in data:
        try:
            airline_dict[datum["AIRLINE"]][1] += 1
        except:
            airline_dict[datum["AIRLINE"]] = [0, 1]
        finally:
            if datum["ARRIVAL_DELAY"][0] == "-":
                airline_dict[datum["AIRLINE"]][0] += 1
    airline_list = [(x[0], x[1][0]/x[1][1]) for x in airline_dict.items()]
    # Sort the on-time rate
    airline_list.sort(key=lambda it: it[0])
    airline_list.sort(key=lambda it: it[1], reverse=True)
    return list(airline_list)


if __name__ == "__main__":
    pass
