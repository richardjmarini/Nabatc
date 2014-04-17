#!/usr/bin/env python

from itertools import izip, chain
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from hashlib import md5
from operator import mul

class Document(object):

   stopwords= stopwords.words('english')

   def __init__(self, text, id= None, additional_stopwords= []):

      super(Document, self).__init__()
      
      self.text= text
      self.id= id if id != None else md5(text).hexdigest()
      self.stopwords+= additional_stopwords

      stemmer= PorterStemmer()
      self.tokens= filter(lambda word: stemmer.stem(word.lower()) not in self.stopwords, word_tokenize(self.text))

   def __repr__(self):
  
      return repr(self.text)


class NaiveBaysenClassifier(dict):

   def __init__(self, additional_stopwords= []):

      super(NaiveBaysenClassifier, self).__init__()
      self.stopwords= additional_stopwords

      self.terms= set()
      self.term_matrix= {}
      self.classification_matrix= {}

   def add(self, text, classification, id= None):

      document= Document(text, id, additional_stopwords= self.stopwords) 
      
      if classification not in self.keys():
         self[classification]= {}

      self.terms= self.terms.union(document.tokens)    
      self[classification][document.id]= document

   def remove(self, id):

      del[id]

   def train(self):

      for classification in self.keys():

         self.term_matrix[classification]= [map(lambda term: self.term_frequency(term, document.tokens),  self.terms) for document in self[classification].values()]
         frequency_sum= sum([sum(vector) for vector in self.term_matrix[classification]])
         self.classification_matrix[classification]= [sum(vector) / float(frequency_sum + len(self.terms)) for vector in zip(*self.term_matrix[classification])]
         
         print '>', self.classification_matrix[classification]

   @staticmethod
   def term_frequency(term, tokens):

      term_frequency= tokens.count(term)

      return term_frequency

   def classify(self, text, id= None):

      document= Document(text, id, additional_stopwords= self.stopwords)
      term_matrix= [self.term_frequency(term, document.tokens) for term in self.terms]

      print self.terms
      print term_matrix

      for classification in self.keys():
         print reduce(mul, self.classification_matrix[classification])


if __name__ == '__main__':

   from glob import glob
   from os import path

   nbc= NaiveBaysenClassifier()

   for filename in glob("../documents/*"):
          
      classification= path.basename(filename).split(".")[1]
       
      fh= open(filename, 'r')
      nbc.add(fh.read(), classification)
      fh.close()

   nbc.train()
   nbc.classify("Richie drives a truck")

