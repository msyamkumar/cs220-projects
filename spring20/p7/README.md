# Project 7: Fédération Internationale de Football Association

## Corrections


## Intro

Let's play Fifa20, Python style!  In this project, you will get more
practice with lists and start using dictionaries.  Start by
downloading `test.py` and `Fifa20.csv` (which was adapted from
[this dataset](https://www.kaggle.com/stefanoleone992/fifa-20-complete-player-dataset#players_20.csv)).
This dataset is too large to preview on GitHub (>18K rows), but you can view the
[raw version](https://raw.githubusercontent.com/msyamkumar/cs220-projects/master/spring20/p7/Fifa20.csv)
or using a program such as [Excel](https://github.com/msyamkumar/cs220-projects/blob/master/spring20/p7/excel.md).
You can also preview an example with 100 rows [here](https://github.com/msyamkumar/cs220-projects/blob/master/spring20/p7/preview.csv).
For this project, you'll create a new `main.ipynb` and answer
questions in the usual format.

## The Data

Try to familiarize yourself with the data before starting the
analysis. We have players belonging to a wide range of nationalities
and clubs in Fifa20. As you can see the data includes their
weekly wages, in Euros (yes, wages are per week!), net worth of the
player (in Euros) and the performance rating (score out of 100). For
instance, the player named "Neymar" is associated with Brazil, is
signed up by club "Paris Saint-Germain", and is paid a weekly wage of '€290K'
(290000 Euros).

To ingest the data to your notebook, paste the following in an early cell:

```python
import csv

fifa_file = open('Fifa20.csv', encoding='utf-8')
file_reader = csv.reader(fifa_file)
player_data = list(file_reader)
fifa_file.close()
header = player_data[0]
player_data = player_data[1:]
for row in player_data:
    for idx in [2, 4]:
        row[idx] = int(row[idx])
```

Consider peeking at the first few rows:
```python
print(header)
for row in player_data[:5]:
    print(row)
```

It's up to you to write any functions that will make it more
convenient to access this data.

## Let's Start!

#### Q1: What is the name of the youngest player?

If multiple players have the same age, break the tie in favor of whoever
appears first in the dataset.

#### Q2: What is the name of the highest-paid player?

If multiple players are paid the same, break the tie in favor of whoever
appears first in the dataset.

#### Q3: What is the name of the highest valued player?

#### Q4: What is the position of that player (in above q3)?

---

Complete the following function in your notebook:

```python
def get_column(col_name):
    pass # replace this
```

The function extracts an entire column from `player_data` to a list, which
it returns.  For example, imagine `player_data` contained this:

```python
[
    ["a", "b", "c"],
    ["d", "e", "f"],
    ["g", "h", "i"]
]
```

And `header` contains this:

```python
["X", "Y", "Z"],
```

Then column "X" is `["a", "d", "g"]`, column "Y" is `["b", "e", "h"]`, and
column "Z" is `["c", "f", "i"]`.  A call to `get_column("Y")` should
therefore return `["b", "e", "h"]`, and so on.

----

#### Q5: What are the first five clubs listed in the dataset?

Use `get_column`, then take a slice from the list that is returned to you.

#### Q6: Which six names are alphabetically first in the dataset?

By alphabetically, we mean according to Python (e.g., it is true that
`"B" < "a"`), so don't use the `lower` method or anything.

Don't deduplicate names in this output in the case that multiple
players have the same name.

#### Q7: What is the average Wage?

#### Q8: What is the average Overall?

---

Define a function `player_count` that takes a parameter, `position`,
and counts the number of players who play in that position. This
function will be useful for the questions that follow.

---

#### Q9: How many players play in the position 'GK'?

#### Q10: How many players play in the position 'CAM'?

#### Q11: Which is the most common position among the players in FIFA20?

The `player_count` function can be useful here.

Hint 1: Make sure you aren't calling `player_count` more times than
necessary.  If you're not careful, the code will be very slow to
execute!

Hint 2: There are multiple ways to implement your code. Try to find the best way!

----

Define a function `player_to_dict` that takes a parameter,
`player_id`, and returns a dict containing all the information about
the player that matches.  Find the player row by matching `player_id`
to the `ID` column in the data.

---

#### Q12: what are the stats for the player with `ID` equal to '183277'?

Use your `player_to_dict` function.  The output should be a dictionary
like this:

```python
{'ID': '183277',
 'Name': 'E. Hazard',
 'Age': 28,
 'Nationality': 'Belgium',
 'Overall': 91,
 'Club': 'Real Madrid',
 'Position': 'LW',
 'Value': '€90M',
 'Wage': '€470K',
 'Preferred Foot': 'Right',
 'Jersey Number': '7',
 'Height': "5'9",
 'Weight': '163lbs'}
```

#### Q13: What are the stats for the player with `ID` equal to '209331'?

#### Q14: What are the stats for the player with `ID` equal to '195864'?

#### Q15: What are the stats for the player with `ID` equal to '177003'?

#### Q16: How many players prefer their right foot and how many players prefer their left foot?

Answer in the form of a dictionary.

#### Q17: How many players are there per Nationality?

Answer in the form of a dictionary. The keys should be the countries and
the values should be the number of players from each country. It should look like:

```python
{'Argentina': 886,
 'Portugal': 344,
 'Brazil': 824,
 'Slovenia': 61,
 'Belgium': 268,
 'Germany': 1216,
 }
```

----

For the following questions, your lab work will be especially useful.

#### Q18: What is the average player score (represented by the `Overall` column) per Nationality?

Answer with a dict, mapping Nationality to average score.

#### Q19: Which Nationality has the highest average Overall?

#### Q20: Which Club has the highest average Value?
