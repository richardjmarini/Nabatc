#Nabatc

###Naive Bayes text Classifier

Naive Bayes Text Classifier help us classify unstructured documents.  The documents directory contains 7 sample documents.  These 7 documents were obtained by crawling Yelp's serach results for "Restaurants in Manhattan".  The crawler was built using the Impetus Framework found here:

https://github.com/richardjmarini/Impetus

The simple sample crawler can found here:

https://github.com/singleplatform/Impetus

The "business provided" blurb was then extracted from the documents.
These blurbs are what you'll find in the documents directory of this project:

https://github.com/richardjmarini/Vespse/tree/master/documents

You'll notice the document contain only the blurb and all the structure has been stripped away.  The documents are as folows:
```
0.txt: a french restaurant
1.txt: a french restaurant
2.txt: a french restaurant
3.txt: a spanish restaurant
4.txt: a spanish restaurant
5.txt: a spanish restaurant
6.txt: a Japanese resturant
```

Based on the probabilities of certain words appearing in the training documents above we can then pass in a query and classify that query:

###Simple Example Usage:
```
$ ./classify.py --query="Classic french food with an american flare"
('french', 5.409541924810811e-07)
('spanish', 6.695169879491226e-09)
('japanese', 6.649172074349659e-09)
```

As you can see, it is the highest probablity that the query passed in describes a French restaurant.

###Another example:
Lets use document 0.txt (which is a french resturant) and classify it:
```
$ cat ../0.txt | ./classify.py
('french', 8.946582439017758e-303)
('japanese', 0.0)
('spanish', 0.0)
```

That's about it!

I'd really like to eat some  rice right now. What type of restaurant should I goto?
```
$ ./classify.py --query="rice"

('japanese', 0.0010277492291880781)
('french', 0.0008836524300441826)
('spanish', 0.0008503401360544216)
```

