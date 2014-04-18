#!/usr/bin/env python

from itertools import izip, chain
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from hashlib import md5
from operator import mul
from math import pow

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

      print 'terms', self.terms
      for classification in self.keys():

         self.term_matrix[classification]= [map(lambda term: self.term_frequency(term, document.tokens),  self.terms) for document in self[classification].values()]
         frequency_sum= sum([sum(vector) for vector in self.term_matrix[classification]])
         self.classification_matrix[classification]= [(sum(vector) + 1) / float(frequency_sum + len(self.terms)) for vector in zip(*self.term_matrix[classification])]
         
         print 'train', classification, self.classification_matrix[classification]
      print "---------------------------------------------"

   @staticmethod
   def term_frequency(term, tokens):

      term_frequency= tokens.count(term)

      return term_frequency

   def classify(self, query, id= None):

      document= Document(query, id, additional_stopwords= self.stopwords)
      query_matrix= [self.term_frequency(term, document.tokens) for term in self.terms]

      print 'query matrix', query_matrix

      total_documents= sum([len(documents) for documents in self.values()])
      for classification in self.keys():
         yield (classification,  (len(self[classification]) / float(total_documents)) * reduce(mul, map(lambda p: pow(*p),  izip(self.classification_matrix[classification], query_matrix))))


if __name__ == '__main__':

   from glob import glob
   from os import path

   nbc= NaiveBaysenClassifier()

   for filename in glob("../documents/*"):
          
      classification= path.basename(filename).split(".")[1]
       
      fh= open(filename, 'r')
      data= fh.read()
      fh.close()

      print classification, data

      nbc.add(data, classification)

   nbc.train()

   query= "The sky had a nice shade of blue"
   print "query:", query
   for classification in nbc.classify(query):
      print classification

