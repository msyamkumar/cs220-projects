# Stage 1: Web and Pandas

In this stage, you will learn about Pandas DataFrames, and answer various questions about the data using dataframes.
<!-- write code to scrape some data from a webpage, save it in json format -->

Use the `download` function from Lab 10a to pull the data from here (do not manually download): https://raw.githubusercontent.com/msyamkumar/cs220-projects/master/spring20/p10/countries.json
and store it in `countries.json`. Once you have created the file, create a Dataframe `countries` from this file

**Warning**: Make sure your `download` function does not download the file if it already exists. The TAs will manually deduct points otherwise.

*Hint*: `pd.read_json('countries.json')` will return a DataFrame by reading from
 the JSON file. If the file contains lists of dictionaries, each dictionary will be a row in the DataFrame.

 Before you proceed, make sure that `countries.head()` displays the following:

 <img src="imgs/1-1.PNG" width="1000">

#### #Q1: How many countries do we have in our dataset?

#### #Q2: what is the total population across all the countries in our dataset?

*Hint*: Review how to extract a single column as a Series from a
 DataFrame. You can add all the values in a Series with the `.sum()`
 method.

----

Use the `download` function to download https://raw.githubusercontent.com/msyamkumar/cs220-projects/master/spring20/p10/capitals.json
and store it in `capitals.json`. Create a DataFrame named `capitals` from this file. Before you proceed, make sure that `capitals.head()` displays the following:

<img src="imgs/1-2.PNG" width="300">

**Note**: If you are feeling brave, instead of downloading the JSON file directly, download the html file with `download('capitals.html', 'https://raw.githubusercontent.com/msyamkumar/cs220-projects/master/spring20/p10/techslides-snapshot.html')` and parse it with Python to create `capitals.json`. Look up the [Optional Exercises for Stage 1](optional1.md) for more details.

Use `capitals` and `countries` dataframes to answer the following questions.


#### #Q3: What are the capital names in `capitals.json`?

Answer with an alphabetically-sorted Python list.


#### #Q4: What is the capital of Italy?

*Hint*: you can use fancy indexing to extract the row where the
 `country` equals "Italy".  Then, extract the `capital` Series, from
 which you can grab the only value using next(iter(...))

#### #Q5: Which country's capital is Brussels?

#### #Q6: Which 7 countries have the southern-most capitals?

Produce a Python list of the 7, with southernmost first.

*Hint*: look at the documentation examples of how to sort a
 DataFrame with the
 [sort_values](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sort_values.html)
 function.

#### #Q7: Which 10 countries have the capitals closest to the North Pole?


#### #Q8: What is the distance between Camp Randall Stadium and the Wisconsin State Capital?

This isn't related to countries, but it's a good warmup for the next
problems.  Your answer should be about 1.4339 miles.

Assumptions:
* The latitude/longitude of Randall Stadium is 43.070231,-89.411893
* The latitude/longitude of the Wisconsin Capital is 43.074645,-89.384113
* Use the Haversine formula: [http://www.movable-type.co.uk/scripts/gis-faq-5.1.html](http://www.movable-type.co.uk/scripts/gis-faq-5.1.html)
* The radius of the earth is 3956 miles
* You should answer in miles

If you find code online that computes the Haversine distance for you,
great! You are allowed to use it as long as (1) it works and (2) you
cite the source with a comment. Note that we won't help you
troubleshoot Haversine functions you didn't write yourself during
office hours, so if you want help, you should start from scratch on
this one.

If you decide to implement it yourself (it's fun!), here are some tips:
* Review the formula: [http://www.movable-type.co.uk/scripts/gis-faq-5.1.html](http://www.movable-type.co.uk/scripts/gis-faq-5.1.html)
* Remember that latitude and longitude are in degrees, but sin, cos, and other Python math functions usually expect radians.  Consider [math.radians](https://docs.python.org/3/library/math.html#math.radians)
* This means that before you do anything with the long and latitudes make sure to convert them to radians as your FIRST STEP

#### #Q9: What is the distance between Germany and Norway?

For the coordinates of a country, use its capital.

#### #Q10: What are the distances between Switzerland, Netherlands and Spain?

Your result should be DataFrame with 3 rows (for each country) and 3
columns (again for each country).  The value in each cell should be
the distance between the country of the row and the country of the
column. For a general idea of what this should look like, open the
`expected.html` file you downloaded.  When displaying the distance
between a country and itself, the table should should NaN (instead of
0).

#### #Q11: What is the distance between every pair of countries in the South American continent?

Your result should be a table with 12 rows (for each country) and 12
columns (again for each country).  The value in each cell should be
the distance between the country of the row and the country of the
column.  For a general idea of what this should look like, open the
`expected.html` file you downloaded.  When displaying the distance
between a country and itself, the table should should NaN (instead of
0).

#### #Q12: What is the most central country in the South American continent?

This is the country that has the shortest average distance to other countries in South America.

*Hint 1*: Check out the following Pandas functions:
* [DataFrame.mean](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.mean.html)
* [Series.sort_values](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.sort_values.html) (note this is not the same as the DataFrame.sort_values function you've used before)

*Hint 2*: A Pandas Series contains indexed values. If you have a
 Series `s` and you want just the values, you can use `s.values`; if
 you want just the index, you can use `s.index`. Both of these
 objects can readily be converted to lists.

#### #Q13: What is the least central country in South America?

This one has the largest average distance to other countries.

#### #Q14: How close is each country in South America to it's nearest neighbor?

The answer should be in a table with countries as the index and two
columns: `nearest` will contain the name of the nearest country and
`distance` will contain the distance to that nearest country.

*Hint 1*: find a Series of numerical data you can experiment with
 (perhaps from one of the DataFrames you've been using for this
 project).  If your Series is named `s`, try running `s.min()`.
 Unsurprisingly, this returns the smallest value in the Series.  Now
 try running `s.idxmin()`.  What does it seem to be doing?

*Hint 2*: if you run `df.min()` on a DataFrame, Pandas applies that
 function to every column Series in the DataFrame.  The returned value
 is a Series.  The index of the returned Series contains the columns
 of the DataFrame, and the values of the returned Series contain the
 minimum values.  If you run `df.idxmin()` on a DataFrame, the
 returned values contain indexes from the DataFrame.

*Hint 3*: if you get an error message about dtypes when running
 idxmin, make sure your DataFrame contains only floats (use
 `df.astype(float)` if necessary).

#### #Q15: How far is each country in South America to it's furthest neighbor?

 The answer should be in a table with countries as the index and two
 columns: `furthest` will contain the name of the furthest country and
 `distance` will contain the distance to that furthest country.

That's it for Stage 1. Please attempt the [Optional1](optional1.md) for further practice.
