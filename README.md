# SI 100B Homework 0: System Setup

* Last modified: Sep. 6, 2020
* Deadline: TBA

## Introduction

This is a dummy homework for you to get familiar with the grading system and set up your local Python programming environment. Before you proceed, please make sure that you have set up your local Python environment and registered for the auto-grader following the [manual](https://si100b.org/content/gitlab-manual.pdf). Please also verify your student ID, email and real name in the grading system. You may receive no point for this and the following programming assignments if your information in the system is wrong or incomplete.

## Getting Started

To get started, please go to the auto-grader, clone your homework repository and set it up from the framework as described in the Repository Structure section. 

*Note*: Markdown text within ***.md*** files could be displayed properly using plug-ins in your browsers, IDEs or specialized markdown editors (like [typora](<https://typora.io/>)).

## Repository Structure

### README.md

Homework descriptions and requirements.

### run.py

A simple ready-to-run Python program that will print a simple pattern on your terminal.

### test.py

The template files in which you fill in your code. 

### output.txt

The template file for your to fill in the output of `run.py`.

## Submission

**You should check in test.py and output.txt to auto-grader.**

First, make a commit from your files. From the root folder of this repo, run

```sh
git add test.py output.txt
git commit -m '{your commit message}'
```

Then push your code to the auto-grader to create a submission. Every push creates a new submission in the system.

```sh
git push
```

You can track your submissions on the web interface of the auto-grader.

## Regulations

- No late submissions will be accepted.
- You have 30 chances of grading (i.e. `git push`) in this homework. If you hand in more 30 times, each extra submission will lead to 10% deduction in your score. In addition, you are able to request grading at most 10 times every 24 hours.
- We enforce academic integrity strictly. **DO NOT** try to hack the auto-grader in any way. You can view the full version of the code of conduct on [Course Webpage](https://si100b.org/resource-policy/#policies).
- If you have any questions about this homework, please ask it on Piazza first so that everyone else can benefit from your question and the answer.

## Specification

Before you start, please follow the instructions in lecture and discussion (and possibly some online resources) to set up the Python interpreter, git and your editors.

### Task 1: Run Python Program

The first thing for you to do in this homework is to run an ready-to-run Python program. The program is provided for you at `run.py`. This program will help you determine whether your local system is ready for SI100B.

Simply run this program with your Python interpreter by

```shell
python3 run.py
```

If the program thinks your setup has problems, it will exit at the place where the problem is found and ask you to fix it. If your system is all set, you will see a ASCII art welcome banner. In this case, copy and paste **all** the output from the last successful run into `output.txt`.

### Task 2: Hello World!

#### Input & Output

* Your program takes no input;
* The output should be exactly the same as "Hello, SI100B!" with no leading or trailing spaces but a newline character at the end(it will be automatically added by `print` function).

Once you finish your implementation, test it in the console by

```sh
python3 test.py
```

You will see

```
Hello, SI100B!
```

if your implementation is correct.

## Feedbacks

* If you find any mistake in this homework, please contact with us directly. Any mistake and typo will be corrected ASAP.
* Comments on this homework are always welcomed so that we could do better. You are also welcome to send us feedback anonymously if you like.
