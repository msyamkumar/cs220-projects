
# OPTIONAL QUESTIONS

These questions have been made optional due to the COVID-19 situation. These questions are not extra credit! We are leaving these as optional for you to get additional practice. You should attempt these questions after Stage 1.

#### Question 1: BeautifulSoup
Very often, you dont have data in nice json format like `capitals.json`. Instead data needs to be scraped from a webpage and requires some cleanup.
This is a long but fun exercise where we will do the same by scraping this webpage: http://techslides.com/list-of-countries-and-capitals.
Our `capitals.json` file was created from this same webpage.
You need to write the code to create `capitals.json` file from this table yourself.
Start by installing BeautifulSoup using pip, as discussed in class.

Then call `download('capitals.html', 'https://raw.githubusercontent.com/msyamkumar/cs220-projects/master/spring20/p10/techslides-snapshot.html')`
to download the webpage. Note that this code is not downloading the original webpage, but a snapshot of it (this is to avoid creating
excessive load on their servers).  You can open `capitals.html` and make sure that this page looks fine.

Now do the following:
* Read from `capitals.html` and use beautiful soup to convert the html text to soup.
* Find the table containing the data (Hint: .find() or .find_all() methods can be used).
* Find all the rows in the table (Note: rows are inside 'tr' html tag and data is in 'td' tag).
* Create a dictionary containing country name, capital and location coordinate. Create a list of dictionaries for all the countries.
* **Careful!** This web page has more countries than `countries.json`. We will ignore the countries that are not in that file. You need to filter and keep only the 174 countries whose names also appear in `countries.json`.
* Save this list into file titled `capitals.json`. You can use json.dump() method.

#### Question 2: What is the largest land-locked country in Africa?

A "land-locked" country is one that has zero coastline. Largest is in terms of **area**.

Expected answer:
```
'Chad'
```

#### Question 3: What is the smallest coastal country in Asia?

A "coastal" country is one that has non-zero coastline. Smallest is in terms of **area**.

Expected answer:
```
'Maldives'
```

#### Question 4: What is the most populous coastal country in South America?

Expected answer:
```
'Brazil'
```

#### Question 5: For `birth-rate` and `death-rate`, what are various summary statistics (e.g., mean, max, standard deviation, etc)?

*Format*: use the
 [describe](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.describe.html)
 function on a DataFrame that contains `birth-rate` and `death-rate`

 columns. You may include summary statistics for other columns in
 your output, as long as your summary table has stats for birth-rate and
 death-rate.

 <table border="1" class="dataframe">
   <thead>
     <tr style="text-align: right;">
       <th></th>
       <th>birth-rate</th>
       <th>death-rate</th>
     </tr>
   </thead>
   <tbody>
     <tr>
       <th>count</th>
       <td>174.000000</td>
       <td>174.000000</td>
     </tr>
     <tr>
       <th>mean</th>
       <td>22.463851</td>
       <td>9.625172</td>
     </tr>
     <tr>
       <th>std</th>
       <td>11.278992</td>
       <td>5.187143</td>
     </tr>
     <tr>
       <th>min</th>
       <td>8.250000</td>
       <td>2.410000</td>
     </tr>
     <tr>
       <th>25%</th>
       <td>12.597500</td>
       <td>6.027500</td>
     </tr>
     <tr>
       <th>50%</th>
       <td>20.010000</td>
       <td>8.230000</td>
     </tr>
     <tr>
       <th>75%</th>
       <td>29.860000</td>
       <td>11.715000</td>
     </tr>
     <tr>
       <th>max</th>
       <td>50.730000</td>
       <td>29.740000</td>
     </tr>
   </tbody>
 </table>

