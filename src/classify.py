#!/usr/bin/env python
#---------------------------------------------------------------------------
#   Author: Richard J. Marini (richardjmarini@gmail.com)
#   Date: 04/18/2014
#   Name: Nabatc (Naive Bayes Text Classification)
#   Description:  A simple Naive Bayes Text Classifier
#   Development Resources:
#       http://en.wikipedia.org/wiki/Naive_Bayes_classifier
#       http://suanpalm3.kmutnb.ac.th/teacher/FileDL/choochart82255418560.pdf
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

from optparse import OptionParser, make_option
from glob import glob
from os import path, pardir, curdir
from sys import argv, stdin, stderr, stdout
from re import sub

from nabatc import NaiveBayesClassifier

def parse_args(argv):

   optParser= OptionParser()

   [optParser.add_option(opt) for opt in [
      make_option("-d", "--documents", default= path.join(pardir, "documents", "*.*"), help= "documents directory"),
      make_option("-q", "--query", default= stdin, help= "query to use for search")
   ]]

   optParser.set_usage("%prog --query")

   opts, args= optParser.parse_args()
   if opts.query == stdin:
      setattr(opts, "query", stdin.read().lower())

   return opts


if __name__ == '__main__':

   opts= parse_args(argv)

   nbc= NaiveBayesClassifier()

   [nbc.add(sub("\n", "", open(filename).read().lower()), path.basename(filename).split(".")[1]) for filename in glob(opts.documents)]

   nbc.train()

   query= "The sky had a nice shade of blue"
   print "query:", opts.query
   for classification in nbc.classify(opts.query):
      print classification
