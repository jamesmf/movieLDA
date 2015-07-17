# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 08:14:44 2015

@author: jmf
"""

import sys
import cPickle
from helper_funcs   import  *
from os.path        import  isfile
from os             import  listdir



#read in .txt of just the records which OMIM has designated with a "#"
#which signifies that "the entry contains the description of a gene of known sequence and a phenotype"

docList =   []

if len(sys.argv) > 1:    
    print sys.argv[1]
    cutoff   =   sys.argv[1]

p   =   "../data/processed/"
l   =   listdir(p)
fileList    =   [p+f for f in l]
    
for x in fileList:
    if isfile(x):
        with open(x,'rb') as f:
            temp =   f.read()
            docList.append(temp)
    
#if isfile("../data/WikiDocs.pickle"):
#    with open("../data/WikiDocs.pickle") as f:
#        wd  =   cPickle.load(f)

whole_str   =   ""
for doc in docList:
    whole_str+=doc.lower()
    
print "before"
file_list_to_lda(whole_str,int(cutoff),stop="yes")
print "after"
    
