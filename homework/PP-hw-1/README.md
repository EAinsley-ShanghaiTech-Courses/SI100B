# SI 100B Homework 1: Flight Analytics

- **Last Modified:** Sept. 15, 2020
- **Release Time:** Sept. 15 2020 23:59 CST
- **Deadline:** Oct. 2 2020 23:59 CST

# Introduction
Python is a powerful programming language that can facilitate jobs including data analysis, as you will experience in this assignment. 

The data that you are going to process is the *Report of Carrier On-Time Performance* (承运人准点率报告) in the United States published by Bureau of Transportation Statistics (运输统计局) of Department of Transportation (运输部). This report includes all of the flight data from 1987 to present for all air carriers (承运人 i.e., airlines, 航空公司)  in U.S.. This database includes flight number (航班号), scheduled departure time (计划出发时间), actual departure time (实际出发时间), distance (距离) and other information for all flights. You can refer to https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236 for more information about fields in the report. The meaning of some fields is in the table below. Notice that some fields in the report are filtered out for this homework and we only provide the following part of the flight data to you.

| Field                                      | Meaning                                                                                                                                           |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AIRLIINE`                                 | The airline of the flight, in the [IATA carrier code](https://en.wikipedia.org/wiki/List_of_airline_codes).                                       |
| `FLIGHT_NUMBER`                            | The flight number(航班号).                                                                                                                        |
| `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT`    | The origin/destination airport in the [IATA airport code](https://en.wikipedia.org/wiki/IATA_airport_code).                                       |
| `SCHEDULED_DEPARTURE`, `SCHEDULED_ARRIVAL` | The **scheduled** departure and arrival time in the format of `hhmm`. For example, 09:08 is represented as `908` and 00:05 is represented as `5`. |
| `DEPARTURE_TIME`, `ARRIVAL_TIME`           | The **actual** departure and arrival time in the format of `hhmm`.                                                                                |
| `DISTANCE`                                 | The distance between departure airport and arrival airport, in miles.                                                                             |
| `DEPARTURE_DELAY`, `ARRIVAL_DELAY`         | The delay time of the flight, in minutes. Negative delay means the flight departs / arrives before the scheduled time.                            |

The data is stored in a CSV (comma separated value) file. The CSV file usually contains multiple rows. For every row, there are multiple columns of fields. In a row, different fields are separated by a single comma (`,`). Each row of data ends with a `\n` (newline) in Python. You should **ignore the empty lines** in the file. The first row in the CSV file is the header, which gives the corresponding keys to each of the columns. The following lines in the file should be regarded as data. An example of a CSV file is given in the repo. The files given to you in testcases are all encoded with `utf-8` (a coding format) without empty columns. An empty column appears when there is no data between two commas or two spaces, e.g.,  `,,`.

In this homework, you are going to write your code to read in the flight data from the CSV file and complete 3 data analysis tasks. Let's get started and have fun!
# Getting Started
To get started, please simply fork the [repository](http://gitlab.q71998.cn/homework-fall2020/homework1) on GitLab and follow the structure and submissions guidelines below and on Piazza.

Remember to make your repository private before making any commits.

Note: Markdown text with file extension .md could be displayed properly using plug-ins in your browsers, IDEs or specialized markdown editors (like typora).
# Repository Structure
* `README.md`: This file. The specification for this homework;
* `analysis.py`: The template file for your submission;
* `data/sample.csv`: The sample data for your to write your own tests. Different from the dataset we use for test your program in the Auto-grader.

## Submission

**You should check in analysis.py to auto-grader.**

First, make a commit from your files. From the root folder of this repo, run

```shell
git add analysis.py
git commit -m '{your commit message}'
```

Then add a tag to create a submission.

```shell
git tag {tagname} && git push origin {tagname}
```

You need to define your own submission tag by changing `{tagname}`, e.g.

```shell
git tag first_trial && git push origin first_trial
```

**Please use a new tag for every new submission.**

Every submission will create a new GitLab issue, where you can track the progress.

## Regulations

- No late submissions will be accepted.
- You have 30 chances of grading (i.e. `git push`) in this homework. If you hand in more 30 times, each extra submission will lead to 10% deduction in your score. In addition, you are able to request grading at most 10 times every 24 hours.
- We enforce academic integrity strictly. **DO NOT** try to hack the auto-grader in any way. You can view the full version of the code of conduct on [course webpage](https://si100b.org/resource-policy/#policies).
- If you have any questions about this homework, please ask it on Piazza first so that everyone else can benefit from your question and the answer.
# Specification
# Task 0: Set up and Read in Data
In this task, you are required to read in data from a CSV file into your program. The sample data will be provided in your repository. The data is includes flight information such as the flight number, departure delay, and arrival time.

This task requires you to read in the data from a file on the disk and store the data in a structured way. That means you need to parse the data you read in from the file as a single string and store the data you read in to data structures like dictionary, list, tuple and so on (or any combination of them). In other words, you are going to *parse* the CSV data you read in in this function. The information in CSV file is recommended to be separated as two parts, keys (i.e., the first line in the CSV) and data rows (i.e., the following lines).

You should take into consideration how you access the data in the following tasks.

Implement this task in `read_csv_for_data(filename)`. The function takes in one parameter filename indicating the file name of the file you need to read in and should return the result in your own format. Designing a good scheme that could save you tons of time in the following tasks. The routines for reading in the CSV table from `filename` has been written for you. You are expected to implement rest part of this function all by yourself. The built-in library `csv` is not allowed in this homework.


# Task 1: Who Flies More than 1500 Miles?
After you read in the data from the CSV file, you will start to perform data analysis. The first step is filtering the data.

In this task, you are going to find out the distance of flights that are more than 1500 miles in the CSV file. You are expected to return the flights number of the flights satisfy the condition as a list. In aviation industry, agents usually represent the flight with the combination of the carrier IATA code (e.g., `CA` for Air China) and the flight number within the carrier (e.g., `1948`). For example, `CA1948` is used to represent the flight number 1948 of Air China. You should follow the convention in your returned value.

In other words, you need to find all the flights with **more than 1500 miles in distance** and return the **concatenation of their `AIRLINE` and `FLIGHT_NUMBER` as strings** inside a list, which is ordered in ascending order of their distance. If the distance between two flights are the same, they should be ordered in ascending order of the **concatenation of their `AIRLINE` and `FLIGHT_NUMBER`** (lexicographic order).

Implement this task in `task1(filename)`. The function takes in one parameter `filename` indicating the file name of the file you need to read in and should return the result as a list of flight numbers as strings in ascending order of their distances.


### Sample Testcase
* Content of the input CSV data file `sample.csv`:

```csv
YEAR,AIRLINE,FLIGHT_NUMBER,TAIL_NUMBER,ORIGIN_AIRPORT,DESTINATION_AIRPORT,SCHEDULED_DEPARTURE,DEPARTURE_TIME,DEPARTURE_DELAY,TAXI_OUT,WHEELS_OFF,ELAPSED_TIME,DISTANCE,WHEELS_ON,TAXI_IN,SCHEDULED_ARRIVAL,ARRIVAL_TIME,ARRIVAL_DELAY
2011,GS,     98,           N407S,      ANC,           SEA,                5,                  2354,          -11,            21,      15,        194,         1448,    404,      4,      430,              408,         -22
2012,AA,     2336,         NKUAA,      LAX,           PBI,                10,                 2,             -8,             12,      14,        279,         2330,    737,      4,      750,              741,         -9
2013,SS,     840,          N17US,      SFO,           CLT,                20,                 18,            -2,             16,      34,        293,         1896,    800,      11,     806,              811,         5
2014,CA,     258,          N3HAA,      LAX,           MIA,                20,                 15,            -5,             15,      30,        281,         2142,    748,      8,      805,              756,         -9
2015,QS,     135,          N527S,      SEA,           ANC,                25,                 24,            -1,             11,      35,        215,         1348,    254,      5,      320,              259,         -21
2015,NK,     451,          N633NK,     PBG,           FLL,                155,                139,           -16,            10,      149,       191,         1334,    443,      7,      523,              450,         -33
2015,NK,     972,          N606NK,     PHX,           DFW,                159,                158,           -1,             11,      209,       125,         868,     452,      11,     502,              503,         1
2015,AA,     1323,         N3CXAA,     MCO,           MIA,                510,                507,           -3,             14,      521,       55,          192,     559,      3,      613,              602,         -11
```
* Function return:

```python3
['SS840', 'CA258', 'AA2336']
```

# Task 2:  Information Filtering

In task two, you will perform more complex filtering

You need to implement `task2` function which has 4 parameters: `filename`,  `airline`,  `key`,  `value`.

This function should return the number of the flights from `airline` (in the format of IATA carrier code), the value of whose `key`  is **less than** `value`. `key` is any field presents in the header (i.e., the first line) of the CSV file. The input `value` is a string, however, if the `key` is a numerical field, we should **convert `value` to number** and compared value of `key` and `value` by its value. Otherwise, we should compare the value of `key` and `value` lexicographically. More specifically, the corresponding value of `YEAR`, `FLIGHT_NUMBER`, `SCHEDULED_DEPARTURE`, `DEPARTURE_TIME`, `DEPARTURE_DELAY`, `TAXI_OUT`, `WHEELS_OFF`, `ELAPSED_TIME`, `DISTANCE`, `WHEELS_ON`, `TAXI_IN`, `SCHEDULED_ARRIVAL`, `ARRIVAL_TIME`, `ARRIVAL_DELAY` should be compared as integers; the corresponding value of `AIRLINE`, `TAIL_NUMBER`, `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT` should be compared as strings. For example, `task2("test.csv", "AA", "FLIGHT_NUMBER", "100")` should return the number of flights from American Airlines (whose IATA code is  `AA`) whose `FLIGHT_NUMBER` is **less than** `100` in`test.csv`. `task2("test.csv", "AA", "TAIL_NUMBER", "NKUAB")` should return the number of flights from American Airlines (whose IATA code is  `AA`) whose `TAIL_NUMBER` is **less than** `'NKUAB'` (lexicographic order) in`test.csv`.

[Lexicographic order](https://en.wikipedia.org/wiki/Lexicographic_order): Compare two strings character by character according to their [ASCII](https://en.wikipedia.org/wiki/ASCII) values.

The function `task2(filename, airline, key, value)` will also need to call `read_csv_for_data(filename)` from Task 0 for data from `filename` at the beginning of the function.

### Sample Testcase

- Input CSV `sample.csv` is the same as the one in Task 1.
- Output:
  - `task2("sample.csv", AA", "YEAR", "2015")` should return `1`.
  - `task2("sample.csv", "AA", "YEAR", "2016")` should return `2`.
  - `task2("sample.csv", "AA", "TAIL_NUMBER", "NKUABa")` should return `2`.

# Task 3: On-time Rate of Airlines

* In task 3, you are required to calculate the on-time rate of each airline in the data file. On-time rate of an airline means the number of flights with `ARRIVAL_DELAY < 0`  from the airline divided by the total number of flights from this airline.

  Implement this task in `task3(filename)`. This function takes a single argument filename indicating the filename of the input CSV file from which you read in the data. The function should return a list of tuples in format of `(airline, rate)` sorted in **decreasing** order of  `rate` which represents the on-time rate of the given `airline`. In your output, `airline` should be in the format of the IATA carrier code of a given airline. If the on-time rate of two airlines happen to be the same, then they should be sorted **lexicographically** in the **increasing** order of `airline`. Your `rate` should have an absolute error of at most $10^{-4}$.

  `task3(filename)` will also need to call `read_csv_for_data(filename)` from Task 0 for data from `filename` at the beginning of the function.

  ### Sample Testcase

  - Input CSV `sample.csv` is the same as the one in Task 1.
  - Output: You should return `[('AA', 1.0), ('CA', 1.0), ('GS', 1.0), ('QS', 1.0), ('NK', 0.5), ('SS', 0.0)]` for this data file.

## Testing and Grading

In the `data` directory we provided you with some simple data and tests for you to examine the correctness of your code. Those tests are pretty simple and naïve. Passing them does not guarantee that you will pass test cases in the auto-grader on your submission. Also, we will use a **different** set of data to test your program. **So read carefully about the specification and create your own reasonable testcase, and do not use the auto-grader as your debugging tool.**

To help your find out which part of your code may be wrong in hope to reduce the time consumption of you on this homework, each testcase will have a label indicating which task the testcase is focusing on. The label will be in the form of `m-n`. For example, the label `2-1` means this testcase is the 1st testcase aiming to test your implementation in task 2.

Good luck!

## Feedbacks

- If you find any mistake in this homework, please contact us directly. Any mistakes or typos will be corrected ASAP.
- Comments on this homework are always welcomed so that we could do better. You are also welcome to send us feedback anonymously if you like. Refer to the [course homepage](https://si100b.org) for feedback channels.