#!/usr/bin/env python
#---------------------------------------------------------------------------
#   Author: Richard J. Marini (richardjmarini@gmail.com)
#   Date: 04/18/2014
#   Name: Nabatc (Naive Bayes Text Classification)
#   Description:  A simple Naive Bayes Text Classifier
#   Development Resources:
#	http://en.wikipedia.org/wiki/Naive_Bayes_classifier
#	http://suanpalm3.kmutnb.ac.th/teacher/FileDL/choochart82255418560.pdf
#
#   License:
#      Nabatc is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 2 of the License, or
#      any later version.
#
#      Nabatc is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Nabatc.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------------------------------------------

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


class NaiveBayesClassifier(dict):

   def __init__(self, additional_stopwords= []):

      super(NaiveBayesClassifier, self).__init__()
      self.stopwords= additional_stopwords

      self.terms= set()
      self.term_matrix= {}
      self.classification_matrix= {}

   def add(self, text, classification, id= None):

      print classification, text

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

         self.term_matrix[classification]= [map(lambda term: self.term_frequency(term, document.tokens), self.terms) for document in self[classification].values()]
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
         yield (classification,  (len(self[classification]) / float(total_documents)) * reduce(mul, map(lambda p: pow(*p), izip(self.classification_matrix[classification], query_matrix))))
