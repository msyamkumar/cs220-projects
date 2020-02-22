# Project 5: Hurricane Study
<!-- ## Under Construction. Dont start working on it before release -->


## Corrections/Clarifications

* **(2/19/2020 4:00 pm)** `test.py` updated. Please download the file again.

## Overview

Hurricanes often count among the worst natural disasters, both in terms of
monetary costs and, more importantly, human life.  Data Science can
help us better understand these storms.  For example, take a quick
look at this FiveThirtyEight analysis by Maggie Koerth-Baker:
[Why We're Stuck With An Inadequate Hurricane Rating System](https://fivethirtyeight.com/features/why-were-stuck-with-an-inadequate-hurricane-rating-system/)
(you should all read FiveThirtyEight, btw!).

For this project, you'll be analyzing data in the `hurricanes.csv`
file.  We generated this data file by writing a Python program to
extract stats from this page:
https://en.wikipedia.org/wiki/List_of_United_States_hurricanes.  By
the end of this semester, we'll teach you to extract data from
websites like Wikipedia for yourself.

This project will focus on **loops** and **strings**. To start,
download `project.py`, `test.py` and `hurricanes.csv`.  You'll do your
work in Jupyter Notebooks this week, producing a `main.ipynb` file.
You'll test as usual by running `python test.py` to test a
`main.ipynb` file (or `python test.py other.ipynb` to test a notebook
with a different name).  You may not use any extra modules that you
need to install with pip (only the standard modules that come with
Python, such as `math`).

We won't explain how to use the `project` module here (the code in the
`project.py` file).  The lab this week is designed to teach you how it
works.

This project consists of writing code to answer 20 questions.  If
you're answering a particular question in a cell in your notebook, you
need to put a comment in the cell so we know what you're answering.
For example, if you're answering question 13, the first line of your
cell should contain `#q13`.

## Questions and Functions

For the first three questions, you don't have to define
any functions of your own. Instead you should just make use of the
functions provided in the file `project.py` by calling the corresponding
function that you need to solve a particular problem.

### Q1: How many records are in the dataset?

### Q2: What is the name of the hurricane at last index?

### Q3: How many deaths were caused by the hurricane at index 10?

### Q4:Is there a hurricane named Bob?

To get full credit on this one, you are required to use a `break` to
finish your loop early if Bob is found. Output `True` if Bob is found and
`False` if the hurricane is not found.

Hint: here's a loop that prints every hurricane name.  Consider
adapting the code?

```python
for i in range(project.count()):
    print(project.get_name(i))
```

### Q5: How many hurricanes named Florence are in the dataset?

Write your code such that it counts all the variants (e.g., "Florence",
"FLORENCE", "fLoReNce", etc.).

### Q6: What is the fastest MPH achieved by a hurricane in the dataset?

### Q7: What is the name of that fastest hurricane?

### Q8: What is the damage (in dollars) caused by the fastest hurricane?

Be careful! In the data, the number was formatted with a suffix (like "K", "M" or "B"), but
you'll need to do some processing to convert it to this: `13500000` (an integer)

You need to write a general function that
handles "K", "M", and "B" suffixes (it will be handy later).
Remember that "K" stands for thousand, "M" stands for million, and "B"
stands for billion!
For e.g. your function should convert a string from "13.5M" to 13500000,
"6.9K" to 6900 and so on.

```python
# return index of deadliest hurricane over the given date range
def format_damage(damage):
  # TODO check the last character of the string
  # and then convert it to appropriate integer by slicing and type casting
  pass
```

<!-- ### Q9: How much faster was the fastest hurricane compared to the average speed of all the hurricanes in the dataset?

You need to calculate the average mph speed of all hurricanes and subtract it from fastest mph speed. -->


<!-- ### Q10: How much damage (in dollars) was done by the hurricane Sandy? -->

### Q9: What is the total number of deaths by all the hurricanes in the dataset?

### Function Suggestion:

We suggest you complete a function something like the following to
answer the next several questions (this is not a requirement if you
prefer to solve the problem another way):

```python
# return index of deadliest hurricane over the given date range
def deadliest_in_range(year1, year2):
    worst_idx = None
    for i in range(project.count()):
        if ????:  # TODO: check if year is in range
            if worst_idx == None or ????:  # TODO: it is worse than previous?
                # TODO: finish this code!
    return worst_idx
```

Hint: You can copy the `get_month`, `get_day`, and `get_year`
functions you created in lab to your project notebook if you like.

### Q10: What was the deadliest hurricane between 2010 and 2020 (inclusive)?

For this and the following, count a hurricane as being in the year it
was formed (not dissipated).

### Q11: What was the deadliest hurricane of the 20th century (1901 to 2000, inclusive)?

### Q12: In what year did the most deadly hurricane in the dataset form?

### Q13: How much damage (in dollars) was done by the deadliest hurricane of the 21th century?

### Q14: What were the total damages across all hurricanes in the dataset, in dollars?

### Function Suggestion:

We suggest you complete a function something like the following to
answer the next several questions (this is not a requirement if you
prefer to solve the problem another way):

```python
# return number of huricanes formed in month mm
def hurricanes_in_month(mm):
    num_of_hurricanes = 0
    for i in range(project.count()):
        pass # TODO: finish this code!
    return num_of_hurricanes
```

### Q15: How many hurricanes were formed in the month of June?

### Q16: How many hurricanes were formed in the month of January?

### Q17: Which month experienced the formation of the most number of hurricanes?

### Q18: How many hurricanes were formed in the decade of 1990-1999 (inclusive)?

### Q19: How many years in the history experienced a hurricane that caused more than 200 in deaths?

### Q20: How many years in the history experienced a hurricane that caused more than 10 Billion in damage?

### Good luck with your hurricanes project! :)
