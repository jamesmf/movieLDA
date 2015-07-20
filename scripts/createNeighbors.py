# -*- coding: utf-8 -*-
"""
@author: James Frick

NIH Center for Advancing Translational Sciences
jamesmfrick@gmail.com

Evaluates a model.  Can be used to create topic heatmaps, histograms, or score
a model based on Disease Ontology hierarchy ROC

Argument 1:
    if this is an integer, script will score the PCA/word frequency version,
        using this arg as the first principal component
    else this should be the folder that contains your data
    
Argument 2:
    if doing PCA/word freq, this is the last PC used
    else it should be either:
        1) "runforall" which will perform analysis on all OMIM-DO docs
        2) the name of a disease in which you're interested.
            if this is the case, it will find OMIM entries containing that name
            and ask you which you'd like to search on.
            
The heatmap portion has been entirely commented out in order to avoid reliance
on Matplotlib.  Thus models can be evaluated on machines with fewer libraries.
"""

import sys, cPickle
import helper_funcs
from os import listdir
import numpy as np
import csv


def main():
 
    #f2  =   open("../data/out/doc_topics.txt",'w')
    
    ###########################################################################   
    """READ INPUT PARAMETERS
    #input parameters are :
        #vocab is the dictionary
        #lambda is a matrix of the words for each Topic
        #gamma is a matrix of the topics for each Document
        #search is a term you would like to match in a document title
            #if search contains spaces, it will search on two terms together
            #and by default should sum the two topic vectors"""
    if len(sys.argv) > 1:
        folder      = sys.argv[1]
        vn          = "../data/dictionary.txt"
        vocab       = str.split(file(vn).read())
        lambdap     = folder + "lambda.pickle"
        gammap      = folder + "gamma.pickle"
        fileList    = folder + "fileList.txt"

                    
    else:
        quit
        


    """Read in lambda from provided Pickle"""
    with open(lambdap,'rb') as tl:
        testlambda  = cPickle.load(tl)

        
    ###########################################################################
    """Write out the word distributions for each topic, sorted by the probability
        that a given word 'belongs' to that topic"""
            
    with open(folder+"topics.txt",'w') as f:
        for k1 in range(0,len(testlambda[0])):
            lambdak1 = testlambda[:,k1]
            lambdak1 = lambdak1/sum(lambdak1)
            testlambda[:,k1] = lambdak1

        for k in range(0, len(testlambda)):
            lambdak = testlambda[k, :]
            temp = zip(lambdak, range(0, len(lambdak)))
            temp = sorted(temp, key = lambda x: x[0], reverse=True)
            f.write("topic "+str(k)+"\n")
            
            #Write out the top 100 words per topic
            for i in range(0, 500):
                f.write(str(vocab[temp[i][1]]) +"\t\t\t" + str(temp[i][0])+"\n")
            f.write("\n\n")           

    ###########################################################################      
    """Read in gamma, the document topic distribution"""  

    docTopics = helper_funcs.read_topic_dist(gammap,fileList)
   
    ###########################################################################
    """run through all User documents and find most similar users"""
    for k,v in docTopics.iteritems():
        p   = helper_funcs.get_sim_docs(k,docTopics,KL=True)
        out = '|'.join([x[0] for x in p[:75]])
        
        with open("../data/out/nearest.txt",'a') as f:
            f.write(out+"\n")





if __name__ == '__main__':
    main()
