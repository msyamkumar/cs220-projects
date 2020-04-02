# Stage 1

For the first few questions, we'll ask you to list files.  These
questions have a few things in common:
* any files with names beginning with "." should be excluded
* you must produce a list
* the list must be in reverse-alphabetical order

Some things will vary:
* which directory you'll look at
* whether the list contains simples file names, or paths
* sometimes you'll need to filter to only show files with certain extensions

You may consider writing a single function to answer several questions
(hint: things that change for different questions can often be
represented with parameters).

----

#### #Q1: What are the names of the files present in the `data` directory?

Hint: Look into the `os.listdir` function. Produce a list of file names, sorted in  **reverse-alphabetical**  order.

#### #Q2: What are the paths of all the files in the `data` directory?

In order to achieve this, you need to use the `os.path.join()`
function. Please do not hardcode "/" or "\\" because doing so will
cause your function to fail on a computer that's not using the same
operating system as yours.

#### #Q3: What are the paths of all the JSON files present in `data` directory?

Filter to only include files ending in `.json`

#### #Q4: What are the paths of all the files present in `data` directory, that begin with the phrase `'review'`?

----

We will first try to read the JSON file `products.json`. You might find it useful here, to create a function to read JSON files.

#### #Q5: What are the products in `products.json`?

Your output should look like this:
```python
{'B00QFQRELG': 'Amazon 9W PowerFast Official OEM USB Charger and Power Adapter for Fire Tablets and Kindle eReaders',
 'B01BH83OOM': 'Amazon Tap Smart Assistant Alexa enabled (black) Brand New',
 'B00ZV9PXP2': 'All-New Kindle E-reader - Black, 6" Glare-Free Touchscreen Display, Wi-Fi - Includes Special Offers',
 'B0751RGYJV': 'Amazon Echo (2nd Generation) Smart Assistant Oak Finish Priority Shipping',
 'B00IOY8XWQ': 'Kindle Voyage E-reader, 6 High-Resolution Display (300 ppi) with Adaptive Built-in Light, PagePress Sensors, Wi-Fi - Includes Special Offers',
 'B0752151W6': 'All-new Echo (2nd Generation) with improved sound, powered by Dolby, and a new design Walnut Finish',
 'B018Y226XO': 'Fire Kids Edition Tablet, 7 Display, Wi-Fi, 16 GB, Pink Kid-Proof Case',
 'B01ACEKAJY': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Black',
 'B01AHB9CYG': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Magenta',
 'B01AHB9CN2': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 16 GB - Includes Special Offers, Magenta',
 'B00VINDBJK': 'Kindle Oasis E-reader with Leather Charging Cover - Merlot, 6 High-Resolution Display (300 ppi), Wi-Fi - Includes Special Offers',
 'B01AHB9C1E': 'Fire HD 8 Tablet with Alexa, 8 HD Display, 32 GB, Tangerine - with Special Offers',
 'B018Y229OU': 'Fire Tablet, 7 Display, Wi-Fi, 8 GB - Includes Special Offers, Magenta'}
```

The keys in the above dictionary are the Amazon Standard Identification Numbers (or asin), that Amazon uses to identify its products.

We will now try to read the CSV files that contain the reviews. Once again, you should consider creating a function to read CSV files given the filename. Use this function to read `review1.csv` to see what's in there.

#### #Q6: What is the review *text* of review with id `84440`?

#### #Q7: What is the review *text* of review with id `28615`?

Careful, this one isn't in `review1.csv`. To get full credit, make sure
your code looks through all the CSV files to find the review.

#### #Q8: What file contained the review with id `69273`?

----

Note that the CSV files we have been reading so far do not contain any information about the product that is being reviewed! That information is stored in the JSON files.

Each JSON file stores information about the reviews in the corresponding CSV file. So, `review1.json` stores information about the reviews in `review1.csv`, `review2.json` stores information about the reviews in `review2.csv` and so on. Feel free to take a look at any of these JSON files, to see how the data is stored.

----

#### #Q9: What is the data stored in `sample_reviews.json`?

`sample_reviews.json` contains a subset of the information in `review1.json`. Your output should look like this:

```
{'46663': ['Dmh1589', 'B018Y229OU'],
 '36363': ['Shoot2thril', 'B018Y229OU'],
 '15763': ['Barbara', 'B018Y229OU'],
 '5463': ['Elec8', 'B018Y229OU'],
 '54066': ['Silvrblur', 'B018Y229OU'],
 '33466': ['Trish', 'B018Y229OU'],
 '40869': ['airbear', 'B018Y229OU'],
 '30569': ['lorphe', 'B018Y229OU'],
 '89472': ['felix', 'B018Y229OU'],
 '48272': ['Bull99', 'B018Y229OU']}
```

The keys are the review ids, and the value stored is a list, containing the name of the user who made the review, as well as the asin of the reviewed product.

----

As we can see, the review data is distributed between different files. It would be useful to combine this data.

For the following questions, you'll need to create a new Review type
(using namedtuple). It should have the following attributes:

* id (int)
* username (string)
* asin (string)
* title (string)
* text (string)
* rating (int)
* do_recommend (bool)
* num_helpful (int)
* date (string)

**Warning**: Please ensure you define your namedtuple exactly according to the
specifications above (with the same attributes and data types), or you will be
unable to pass the tests.

You should be able to use your Review type to create new Review objects, like this:

```python
review = Review(38574, "Rebe", "B018Y229OU", "Excellent" , "The tablet is great and works perfectly for any use", 5, True, 0, "2016-01-20")
review
```

Running the above in a cell should produce output like this:

```
Review(id=38574, username='Rebe', asin='B018Y229OU', title='Excellent', text='The tablet is great and works perfectly for any use', rating=5, do_recommend=True, num_helpful=0, date='2016-01-20')
```

----

Build a function `get_reviews` that accepts a CSV review file and a JSON review file and combines them to produce a list of `Review` objects, which it either returns or yields (your choice!).

#### #Q10: What is produced by your function `get_reviews('sample_reviews.csv', 'sample_reviews.json')`?

The output should be a list of ten Reviews. If you chose to write a generator with yield, just convert the generator object to a list.

Be careful, if you get the types wrong for any of the Reviews, the tests won't recognize it.

#### #Q11: What are the first ten Review objects in the list produced by `get_reviews('review4.csv', 'review4.json')`?

#### #Q12: What are the last ten Review objects in the list produced by `get_reviews('review2.csv', 'review2.json')`?

It is likely that your code crashed. That is because the last few rows in the file `review2.csv` are broken. Go back to `get_reviews` and fix it so that broken rows are skipped. To get full credit, you need to skip only the rows that have missing data.

**Hint**: A row could be 'broken' because
1. Some entries in the column are missing. (i.e., some entry is just the empty string.)
2. Some entries in the column are in the wrong column (i.e. the column `rating` contains the value for the column `do_recommend`.)
3. Some entries are meaningless (i.e., a product's `date` is not a date.)

This is not an exhaustive list of all the ways the data can be bad, and you are
not expected to deal with all the possibilities (or even all the possibilities
listed above!). You need to manually look at `review2.csv` (via some Spreadsheet
software), find the ways in which data is 'broken' in that particular file, and
fix your code so that the bad rows are skipped.

**Additional Hint**: Exactly five rows in `review2.csv` have bad data, and they
are all near the bottom of the file.


#### #Q13: What is the Review object with review id `25401`?

#### #Q14: What is the Review object with review id `78626`?

#### #Q15: List the first ten Review objects in the entire dataset, when the usernames are sorted in the reverse alphabetical order.

It is likely that your code crashed when you tried to read some of the files. That is because some of the JSON files are broken. Unlike broken CSV files, broken JSON files are much harder to salvage. Your code should skip any JSON files that you are unable to parse using  `json.load`.

**Hint**: You could use try/except here.

That's it for Stage 1. Please attempt the [Optional questions](optional_questions.md) for further practice.
In the next stage, we'll begin using the data
structures we've set up to do some analysis that spans across multiple
files!
