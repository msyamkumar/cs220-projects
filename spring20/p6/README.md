# Project 6: Wine Study

## Corrections and Clarifications

* **(2/26/2020, 2:00 pm)** Bugs fixed in test.py. Redownload if you have already downloaded.
* **(2/26/2020, 8:20 pm)** Q18 clarified.

## Announcements

* Remember you must begin each cell with the comment #q1, #q2, etc.  This comment is read by test.py to
identify which question is being answered. We recommend copying the entire question line as a comment
into your notebook.
* To view comments grader comments for previous projects go to the project submission page and select
the graded project and click view submission.
* For regrade requests.  First contact the TA who graded your project - you can find their contact
information when you view your submission.
* Please remember that if you are looking for a partner you can use our Match Making service found under surveys on the course webpage.

## Introduction

This project is a wine connoisseurs' delight!  Data Science can help us understand people's drinking
habits around the world.  For example, take a look at Mona Chalabi's analysis
here: [Where Do People Drink The Most Beer, Wine And Spirits?](https://fivethirtyeight.com/features/dear-mona-followup-where-do-people-drink-the-most-beer-wine-and-spirits/)

For our part, we will be exploring a modified subset (the first 1501 rows) of the Kaggle
[wine reviews dataset](https://www.kaggle.com/zynicide/wine-reviews);
you will be using various string manipulation functions that come with
Python as well as rolling some of your own to solve the problems
posed. Happy coding, and remember the [Ballmer
Peak](https://xkcd.com/323/) is nothing but a myth!

## Directions

Be sure to do lab 6 before starting this project; otherwise you
probably won't get very far.

Begin by downloading `wine.csv` and `test.py`.  Create a `main.ipynb`
file to start answering the following questions, and remember to run
`test.py` often.  There is no `project.py` this week, use the code from the lab to access the data.  Remember to use
the `#qN` format as you have for previous projects.

### #Q1: What countries are present in the wine dataset?

Generate a Python list containing the country names. The order of the names doesn't matter but make sure that your answer doesn't contain duplicate entries.

Note: Some entries in the data set are missing country names (real-life data is often messy,
unfortunately!).  Missing values are represented as `None`. Do not include `None` in your answer.

Now is a good time to run the tests with `python test.py`.  If you did Q1 correctly, it should look like this:

```
Summary:
  Test 1: PASS
  Test 2: not found
  Test 3: not found
  Test 4: not found
  Test 5: not found
  Test 6: not found
  Test 7: not found
  Test 8: not found
  Test 9: not found
  Test 10: not found
  Test 11: not found
  Test 12: not found
  Test 13: not found
  Test 14: not found
  Test 15: not found
  Test 16: not found
  Test 17: not found
  Test 18: not found
  Test 19: not found
  Test 20: not found

TOTAL SCORE: 5.00%
```

### #Q2: What is the average price of wine?

Be careful!  There may be missing price information for some rows. Skip rows without price information and do not include them in your calculation.

### #Q3: List all wineries which produce wine in New Zealand?

Answer in the form of a list containing no duplicates!! (for this and future questions).

### #Q4: Which wine varieties contain the phrase "cranberry" in the description?

This should match anything containing "cranberry" (in any case), regardless of
spacing.

### #Q5: Which wine varieties contain the phrase "lemon-lime soda" in the description?


### #Q6: Which wine varieties contain the phrase "black-fruit" in their description?

### #Q7: Which wine varieties are anagrams of the phrase "antibus governance"?

If you liked Professor Langdon's adventures in Da Vinci Code, you'll have fun with this one. :)

An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, using all the original letters exactly once.
(Read more here: https://en.wikipedia.org/wiki/Anagram).  For our
purposes, we'll ignore case and spaces when considering whether two words are anagrams of each other.

Hint: although you'll need to loop over all the names to check for
anagrams, checking whether a single word is an anagram of another word
does not require writing a loop.  So if you're writing something
complicated, review the string methods and sequence operations to see
if there is a short, clever solution.

### #Q8: How many unique wineries, produce the wine variety "Pinot Noir"?

### #Q9: What is the highest-rated wine variety made in "Spain"?

Your answer should be in the form of a Python list.  If there is a single best, that list will contain one entry with that single best variety.  If
multiple varieties tie for best, the list should contain all wines that tie.

### #Q10: Which winery produces the highest-priced wine in "Italy"?

Your answer should be in the form of a Python list.  If there is a single best, that list will contain one entry with that single best variety.  If
multiple wineries tie for best, the list should contain all wineries that tie.

Consider writing a function to solve Q9 and Q10 with the same code.

### #Q11: What is the average points-per-dollar (PPD) ratio of the "Patricia Green Cellars" winery?

In this question, we're trying to find the best value using the
`points` (the rating) and `price` (cost in dollars) columns.

Be careful!  You need to compute the ratio for each wine of the given
winery, then take the average of those ratios.  Simply dividing the
sum of all points by the sum of all prices will calculates the wrong
answer.

Consider writing a function to answer Q11 and Q12

### #Q12: What is the average PPD of the "Hall" winery?

### #Q13: Which wineries in US have the highest average PPD?

Your answer should be in the form of a Python list.  If there is a single best winery, the list will contain one entry.  If multiple wineries tie for best, the list should contain all wineries that tie.

Consider writing a function to answer Q13, Q14, and Q15 with the same code.

### #Q14: Which wineries in South Africa have the highest average PPD?

### #Q15: which wineies in Argentina have the lowest average PPD?

### #Q16: Which wine varieties are produced by the "Ironstone" winery?

Produce a Python list with no duplicates.

Consider writing a function to answer Q16 and Q17 with the same code.

### #Q17: Which wine varieties are produced by the "Quinta Nova de Nossa Senhora do Carmo" winery?

Produce a Python list with no duplicates.

### #Q18: What percentage of wine varieties that contain the word "cranberry" in its description also contain the phrase "black-fruit" in its description? See Q4 and Q6.

The two wines need not be the same. If a wine variety has two wines, one with 'cranberry' in its description, and the other wine with 'black-fruit' in its description, we want to count that wine variety.

### #Q19: What is the price of the most expensive wine that you could find in Portugal?

Ignore the entries which do not include the price value.

### #Q20: What is the total cost of buying two bottles of the most expensive wine and three bottles of the cheapest wine in Portugal?

Cheers!
