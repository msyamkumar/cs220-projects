# Stage 1 OPTIONAL QUESTIONS

These questions have been made optional due to the COVID-19 situation. These questions are not extra credit! We are leaving these as optional for you to get additional practice.

----

#### #Q1: What is the review *title* of review id `69273`?

You should be able to use your Review type to create new Review objects, like this:

Expected answer:
```
'Excellent'
```
----

For this last section, we will now try to combine the data we have stored in the Review objects with the data from `products.json`.

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

That's it for Stage 1. In the next stage, we'll begin using the data
structures we've set up to do some analysis that spans across multiple
files!
