# OPTIONAL QUESTIONS

These questions have been made optional due to the COVID-19 situation. These questions are not extra credit! We are leaving these as optional for you to get additional practice. You should attempt these questions after Stage 1.

----

#### #Q1: What is the review *title* of review id `69273`?

You should be able to use your Review type to create new Review objects, like this:

Expected answer:
```
'Excellent'
```

#### #Q2: Output the number of review objects for the product, 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 16 GB - Includes Special Offers, Magenta'.

Expected answer:
```
975
```
#### #Q3: Output the number of review objects for the product, "All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Magenta".

Expected answer:
```
47
```

#### #Q4: Find the name of the product with most reviews.

Expected answer:
```
'Fire Tablet, 7 Display, Wi-Fi, 8 GB - Includes Special Offers, Magenta'
```
#### #Q5: Find the earliest review(s) of this product.

**Hint**: Note that the dates are stored in the 'yyyy-mm-dd' format.

Expected answer:
```
Review(id=73101, username='Jhun', asin='B018Y229OU', title='Great tablet for my 3 year old twins', text='Very nice product...Had everything we were looking for...', rating=5, do_recommend=True, num_helpful=2, date='2015-11-06')

```
#### #Q6: How many unique usernames appear in the dataset?

Expected answer:
```
3818
```

#### #Q7: Which words appear most commonly in the text of reviews with rating 4. List only the words that appear more than 500 times.

For simplicity, you can use `txt.lower().split(" ")` to get the words from a string `txt` (this counts punctuation as part of a word, which is not ideal, but won't affect the results too greatly).

Answer with a `dict` mapping the words to the number of times they appear in the review text.

Is this data meaningful? Can you think of ways of extracting useful information about the mood of the reviewer from the words in the review text?

Expected answer:
```
{'for': 1020,
 'the': 830,
 'a': 649,
 'i': 577,
 'it': 628,
 'and': 778,
 'to': 716,
 'is': 521}
```

#### #Q8: Which words appear most commonly in the title of reviews with rating 4. List only the words that appear more than 100 times.

Answer with a `dict` mapping the words to the number of times they appear in the review title.

Can you infer anything about the mood of the reviewers who rate products highly? Why couldn't you get this information from the review text so easily?

Expected answer:
```
{'great': 433,
 'for': 433,
 'good': 290,
 'tablet': 363,
 'price': 125,
 'the': 144}
```

#### #Q9: Which words appear most commonly in the title of reviews with rating 2. List the words that appear more than once.

Answer with a `dict` mapping the words to the number of times they appear in the review title.

Do you notice any differences between the two dictionaries?

Expected answer:
```
{'tablet': 4,
 'it': 2,
 'the': 2,
 'fire': 2,
 'you': 6,
 'get': 3,
 'what': 3,
 'pay': 3,
 'for.': 2,
 'average': 2,
 'not': 3,
 'good': 2,
 'for': 3,
 'and': 2,
 'very': 2,
 'charging': 2}
```

#### #Q10: Which words appear most commonly in the title of reviews with rating 3. List only the words that appear more than 10 times.

Answer with a `dict` mapping the words to the number of times they appear in the review title.

What differences and similarities do you see between the words in these three lists? Can you try to find the words that appear most commonly in the title of reviews with other ratings? Do you notice any patterns?

Expected answer:
```
{'tablet': 43,
 'the': 14,
 'great': 27,
 'good': 41,
 'for': 58,
 'price': 16,
 'ok': 17,
 'a': 18,
 'nice': 12,
 'not': 15}
```
