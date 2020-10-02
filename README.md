# SI 100B Homework 2: Flight Analytics

- **Last Modified:** Oct 2, 2020
- **Release Time:** Oct 2, 2020
- **Deadline:** 23:59:00 China Standard Time, Oct 18, 2020

## Introduction

In this homework, you are going to re-implement the Flight Analytics tool you created for the previous homework, extending its generality and robustness by using object-oriented programming and exception handling. It will considerably simplify the operations needed for similar tasks in HW1.

## Getting Started

To get started, please simply fork the repository on GitLab and follow the structure and submissions guidelines below and on the [course homepage](https://si100b.org/pages/gitlab-manual/).

Remember to make your repository private before making any commit.

Note: Markdown text with file extension `.md` could be displayed properly using plug-ins in your browsers, IDEs or specialized markdown editors (like Typora).

## Repository Structure

* `README.md`: This file. The specification for this homework.
* `analysis.py`: The template file for your submission.
* `data/sample.csv`: The sample data file for you to test your program.

## Submission

**Analysis.py will be checked by the auto-grader.**

First, make a commit from your files. From the root folder of this repository, run

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

## Regulation

- You may not use third-party libraries and the built-in library `csv`.
- No late submissions will be accepted.
- You have 30 chances of grading (i.e. git tag) in this homework. If you hand in more than 30 times, each extra submission will lead to 10% deduction. In addition, you are able to require grading at most 10 times every 24 hours.
- We enforce academic integrity strictly. If you participate in any form of cheating, you will fail this course immediately. DO NOT try to hack GitLab in any way. You can view the full version of the code of conduct on the course homepage: https://si100b.org/resource-policy/#policies.
- If you have any question about this homework, please ask on Piazza first so that everyone else could benefit from the question and its answer.

## Specification

### Task 1: Row and Table

In this task, you will first read in some data from a CSV file (which will be provided in your repository) into your program, the same way as what you have done in Task 0 of HW 1.  But after reading in the CSV file, you are going to deal with the data in a more sophisticated yet robust fashion..

In OOP, you often need to organize related data and functions into classes. In this assignment, we define tables in an OOP style. We have a `Table()` class and a `Row()` class. In our definition, A `Table` object consists of a number of `Row` objects, just like a real table consisting of rows. We have defined the `Row(`) class already: it represents a row of data. You will need define the `Table()` class.

When finished, `Row()` and `Table()` will work as follows:

```python
from analysis import Row, Table

row = Row(["ID", "a", "b", "c"], [4, 1, 2, 3]) # Create a row.
print("The row is {} items long.".format(len(row))) # get the row's length
for col in row:  # iterate through the row
  print("Column: {}, Data: {}".format(col, row[col]))

table = Table("data/sample.csv")
# Initalize the table with a CSV data file.
for row in table:
  # Iterate the table on the basis of rows.
  for col in row:
  	print("Row ID: {}, Column: {}, Data: {}".format(row.get_id(), col, row[col]))
```

#### Row()

**The `Row()` class has been implemented  for you in `analysis.py`.** 

It serves as a building block for the `Table()` class. Meanwhile, we suggest you read its code which may help you write the code for `Table()`.  `Row()` implements the following methods:

* `__init__(self, keys, data)`: The `Row()` initializer. It will initialize all the internal data structure of the `Row()` object. The `key` argument should be an iterable of the keys , indicating names of columns. All the items in the `key` argument should be `str`. The `data` argument is also an iterable that contains all the data in the given row. `key` and `data` should be of the same length and the i-th item in `data` should correspond to the i-th item in `key`.

  To uniquely identify a row in a table, for each row, we are adding a special key called `ID` to the data source CSV file. This column is guaranteed to exist and be unique for every row in CSV file.

* `keys(self)`: Return the keys in the row as a tuple;

* `get_id(self)`:Return  the ID field’s value of the row;

* `__getitem__(self, key)`: Return the item corresponding to the `key`.

*  `__setitem__(self, key, value)`: Set the item corresponding to the `key` to the `value`.

* `__iter__(self)`, `__next__(self)`:Implement an iterator on the row. Every time `next(`) calls on the iterator, it will return a column in the table, in the lexicographically ascending order;

* `__lt__(self, other)`: Compare `self` with `other`. Return `True` if and only if `self`'s ID is less than `other`’s. The method will be useful when you are sorting your rows in your `Table()` implementation using `storted()`. In the test case we give, all the `ID` field values support comparison with each other in a single table (more below); 

* `__len__(self)`: Return the number of columns in the row.

* You may define other methods and helper classes as long as they are helpful.

 Demo code showing the Row object’s usage:

```python
from analysis import Row

row = Row(["ID", "b", "c"], [1, 2, 3]) # initalize the row with `key` and `value`.
print("Row length: {} columns".format(len(row)))
for col in row:
      print("Column key: ", col)
      print("Column data: ", row[col])
      
foo = Row(["ID", "b", "c"], [1, 2, 3])
bar = Row(["ID", "b", "c"], [2, 0, 4])
print("If `foo` is less than `bar`?", foo < bar)
```

You can run the code snippet above and explore code in `analysis.py` to explore the implementation of `Row()`.

#### Table()

As we mentioned above, a table usually consists of zero or more rows. The rows in a table must have the same set of columns. In this task, you are going to build your `Table()` object to formalize these requirements..

The `Table()` object should read in the table from a CSV file and divide the table into rows  on which you perform the required operations.

The CSV file usually contains multiple rows. Every row has multiple columns of fields, which are separated by a single comma (`,`) and zero or more spaces before or after it, and ends with a `\n` in Python. You should ignore the empty lines in the file. The first row of the CSV file is the header, which gives the corresponding keys to each of the columns. An example of a CSV file is given in the next part. The files given to you in test cases are all encoded with `utf-8` and they do not have any empty column (empty columns occur when two commas have no data or have pure spaces between them. e.g.,  `,,`). An example CSV file is shown below.

```csv
ID,YEAR,AIRLINE,FLIGHT_NUMBER,TAIL_NUMBER,ORIGIN_AIRPORT,DESTINATION_AIRPORT,SCHEDULED_DEPARTURE,DEPARTURE_TIME,DEPARTURE_DELAY,TAXI_OUT,WHEELS_OFF,ELAPSED_TIME,DISTANCE,WHEELS_ON,TAXI_IN,SCHEDULED_ARRIVAL,ARRIVAL_TIME,ARRIVAL_DELAY
0,2011,GS,     98,           N407S,      ANC,           SEA,                5,                  2354,          -11,            21,      15,        194,         1448,    404,      4,      430,              408,         -22
1,2012,AA,     2336,         NKUAA,      LAX,           PBI,                10,                 2,             -8,             12,      14,        279,         2330,    737,      4,      750,              741,         -9
```

It can be turned into a table:


| AIRLINE | ARRIVAL_DELAY | ARRIVAL_TIME | DEPARTURE_DELAY | DEPARTURE_TIME | DESTINATION_AIRPORT | DISTANCE | ELAPSED_TIME | FLIGHT_NUMBER | ID | ORIGIN_AIRPORT | SCHEDULED_ARRIVAL | SCHEDULED_DEPARTURE | TAIL_NUMBER | TAXI_IN | TAXI_OUT | WHEELS_OFF | WHEELS_ON | YEAR |
| ------- | ------------- | ------------ | --------------- | -------------- | ------------------- | -------- | ------------ | ------------- | -- | -------------- | ----------------- | ------------------- | ----------- | ------- | -------- | ---------- | --------- | ---- |
| GS      | -22           | 408          | -11             | 2354           | SEA                 | 1448     | 194          | 98            | 0  | ANC            | 430               | 5                   | N407S       | 4       | 21       | 15         | 404       | 2011 |
| AA      | -9            | 741          | -8              | 2              | PBI                 | 2330     | 279          | 2336          | 1  | LAX            | 750               | 10                  | NKUAA       | 4       | 12       | 14         | 737       | 2012 |

Your `Table()` class is expected to have the following methods:


* `__init__(self, filename, rows=None, keys=None)`: Initialize your `Table()` object in this method. 

  Argument `filename` is the path to the CSV file to read in, relative to your current working directory. The file will always be available in the file system.  You are allowed to design your own internal attributes as long as they are not accessible from outside.

  Your `__init__()` should support two approaches to construct the `Table()` object. The first one is from a file. This approach should be applied when the third argument `row`s is set to None. You should read in the table from the CSV file specified by filename. All testcase files are guaranteed to be in the system, such that you do not need to worry about the file missing scenario. The second one is from multiple rows. This should be applied when `rows` is set to an iterable that contains a number of instances of the `Row()` object and `keys` is set to a non-empty list of keys in your table. In this case, you should construct your `Table(`) object from those rows and you are not supposed to read the file as specified by `filename`. These two arguments should be ignored if only one of them is presented.

  As you may have noticed, the data fields you read in from the CSV file are all strings. It is not convenient to use strings to perform some operations in the following tasks. So you should convert all fields into an integer except for AIRLINE,TAIL_NUMBER, ORIGIN_AIRPORT, and DESTINATION_AIRPORT fields. As we have performed such operations in class Row(), you do not need to do the conversion if you construct your table from multiple Row() objects;
  
* `keys(self)`: Return the keys in the `Table()` as a list in lexicographically ascending order, same as `keys()` in `Row()`;

* `get_table_name()`: Return the table name of the table. The table's name is the `filename` argument in `__init__()`;

* `__getitem__(self, id)`: Index the table by the id. This method should return the row object instance, whose the `ID` field matches `id`, as a `Row()` object. Raise `ValueError` if the table does not contain such a row. You are not expected to return a copy of the row since we want any modification on the row being reflected in the table (think about why);

* `__iter__(self)`, `__next__(self)`: Implement an iterator on the table. Your iterator should return a Row() object each time the next() method is called on it.  It should loop over the rows inlexicographically ascending order of the ID field;

* `__len__(self)`: Return the number of rows in the table;

* You may define other methods and helper classes as long as they are helpful.

Once you finish your implementation, you can test it like this:

```python
from analysis import Row, Table

table = Table("data/sample.csv")
for row in table:
  for col in row:
  	print("Row ID: {}, Column: {}, Data: {}".format(row.get_id(), col, row[col]))
```

### Task 2: Query on Single Table

Now you need to implement the class `Query` which is used to look for data in a CSV file that satisfies the conditions given by user.

The query from the user is represented as a Python dictionary that contains two parts: the first part is a list of dictionaries containing filtering conditions called `condition`, the second one is the filename of the data source called `filename`.

An example of the query will be

```python
query = {
  "condition": [{
    'key': 'YEAR',
    'value': '2015',
    'operator': '<'
  },
  {
    'key': 'TAIL_NUMBER',
    'value': 'N97W2',
    'operator': '!='
  }],
  "filename": "sample.csv",
}
```

This query tells your program to find all the data rows that is before 2015 and the airplane’s tail number (TAIL_NUMBER, 国籍注册号) is not `N97W2`. More formally, we define the query as following:

-  `condition` contains a list of dictionaries. Each dictionary contains three key-value pairs, `key`, `value` and `operator`. 
  
  - `key` is a string. You should check if the `key`s presented in the condition dictionaries are in the table. If not, raise `KeyError`.
    
  - The `operator`s are strings in the format and of the semantics of the Python conditional operators. Possible operators are `==`, `>`, `<`, `>=`, `<=` and  `!=`. 
    
  
  Each dictionary gives you a *condition*. A condition is telling a way to filter the row by the field `key`. A condition is statisfied for a row if and only if the field corresponding to the `key` satisfy the binary relationship specified by the binary `operator` with `value`. Or as pseudo code: `(row[key] operator value) == True`.
  
  The query result should  include all the rows that satisfy all the conditions in `condition` in the result of the query. If the `condition` list is empty, all the rows in the table should be included. The data type of `key` and `value` is same as in HW 1. The corresponding value of `AIRLINE`, `TAIL_NUMBER`, `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT` should be treated as string and other columns should be treated as integer;
  
- The `filename` points to the CSV file your query would work on. .

Your implementation of the query should be in the class `Query()`.

* `__init__(self, query)`: The initializer of the `Query()` class. `query` is the query you need to perform , in the format we described above;
* `as_table(self)`: Return the result of the query as a `Table()` object named with the original table name in query;
* You may define other methods and helper classes as long as they are helpful.

### Task 3 Data Exportation

We now implement a method for exporting selected columns of the table to a file on your disk, such that it can be preserved for long-term use.

Now in your `Table()` class, implement a method named `export(columns,filename=None)` allowing the exportation of selected columns of the table to a file on the file system.

* `Table.export(columns,filename=None)`: The method takes in two arguments, `columns` and `filename`;

  * `columns` should be a list of column names specified by the user to identify the columns to be exported .If this argument is an empty list, simply export all the columns of the table;

  * `filename` gives you the location where the table should be exported to. If the file exists at the time, overwrite the file. If it does not exist, create it beforehand. If this argument is  `None`, overwrite the original file we read the table data from;

Your exported table should also be a CSV one. The first row of the output file should be the column names. From the second row on, you should output the data rows. Every row is ended with a single `\n` (including the last row). Different fields in the same row should be separated by a single comma ( `,`) without any white spaces in between. The order of fields in a row and between rows in the table should be preserved (i.e., **lexicographical ascending order of field name in first row and ascending order by value in `ID` field for other rows**).

### Bonus: Data Aggregation

You are going to implement data aggregation for your query in this task. This task is a bonus task. Finishing this task will give you an additional 10% in your final score for this assignment.

Sometimes you want to know aggregated quantity in specific groups of rows in the table. For example, you may want to know the average distance of flights for three airlines:American Airlines (AA), Spirit Airlines (NK) and Air China (CA). Of course you could get the flights' distance from all three airlines and use a Python program to calculate the average distance. But here you are doing it with a single query.

The operation we described above is called data aggregation. In this task, you are implementing a new class called `AggQuery()` which is inherited from `Query()`, with aggregation operations on tables. Since it is inherited from `Query()`, `AggQuery()` should provide the same interfaces (methods) as `Query()`.

#### Aggregation

For this task, we use a query dictionary that is similar to the one in task 2 with 3 new keys `column`, `function` and `group_by`.

For example, the following  query tells your program to find all the data rows that is before the year of 2015 and the airplane’s tail number is not `N97W2` and find the maximum distance of flights from all the airlines in the data rows satisfing those conditions.

```python
query = {
    "condition": [{
        'key': 'YEAR',
        'value': '2015',
        'operator': '<'
      },
      {
        'key': 'TAIL_NUMBER',
        'value': 'N97W2',
        'operator': '!='
      }],
  "column": "DISTANCE",
  'function': 'MAX',
  "filename": "sample.csv",
  "group_by": "AIRLINE"
}
```

And when we call the `as_table()` function of above, your implementation should be able to return a `Table()` that exports to a CSV file like the following (different rows' ordering is acceptable).

```csv
AIRLINE,ID,MAX(DISTANCE)
AA,0,1239
SK,1,2431
```

More formally, we define the query as following:

* `column` is the field of data you need to aggregate. If the `column` doesn't exist in the data, raise `KeyError`;

* According to `function`, you perform different operations on the `column` field.  In this task, you need to support only two functions: 

  * `AVG`: get the average value in all the fields of the column;

  *  `MAX`: get the maximum value in the column; 

  The `AVG` function will only be applied to the columns that support both arithmetic addition (`+`) and arithmetic division (`/`), which include all the columns **except** `AIRLINE`, `TAIL_NUMBER`, `ORIGIN_AIRPORT` and `DESTINATION_AIRPORT`. The `MAX` function can be applied to the any columns;

* The `group_by` gives a column name as a string. you need to group up the rows with the same value in the  `group_by` column together and then use the aggregation functions (`AVG` or `MAX`) to calculate the aggregated value of  `column`  of the groups. 

More specifically, the aggregation works the following way: First, you need to filter the data with the `condition` the same way as in task 1. Then group up the rows that is included in the result of last step by the `group_by` field and calculate the required value of the `column` field  with `function`. The corresponding column should be named as `${function} ${column}` (e.g.,`MAX DISTANCE`) in the result table. 

The rows in the result table need an `ID` field since our `Table()` class uses it to distinguish different rows. However, there is no reasonable `ID` for the rows here after data aggregation, so you may assign an arbitrary unique `ID` for every row in the table. In other words, in your implementation, rows can be in any order.

## Testing and Grading

In the `data` directory we provide you with some simple data and tests for you to examine the correctness of your code. Those tests are pretty simple and naïve. Passing them does not guarantee that you will pass test cases in the auto-grader on your submission. Also, we will use a **different** set of data to test your program. **So read carefully about the specifications and create your own reasonable testcase, and do not use the auto-grader as your debugging tool.**

To help your find out which part of your code may be wrong in hope to reduce the time consumption of you on this homework, each testcase will have a label indicating which task the testcase is focusing on. The label will be in the form of `m-n`. For example, the label `2-1` means this testcase is the 1st testcase aiming to test your implementation in task 2.

Good luck!

## Feedbacks

-  If you have any confusion about this assignment, please contact us ASAP.
- Comments on this homework are always welcomed so that we could do better. You are also welcome to send us feedback anonymously if you like. Refer to the [course homepage](https://si100b.org) for feedback channels.
