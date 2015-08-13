# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 12:21:40 2015

take user documents and create a word2vec doc out of it


@author: frickjm
"""
from random import shuffle
import numpy as np


def getRandom(user,words,numLines,numWords,outfile):
    for x in range(numLines):
        shuffle(words)
        new     = ' '.join(words[:numWords/2])+' '+user+' '+' '.join(words[numWords/2:numWords])
        with open(outfile,'a') as of:
            of.write(new+'\n')

def main():
    NUMWORDS    = 20
    NUMLINES    = 1000
    OUTFILE     = "../data/W2V_movies.txt"
    folder      = "../data/out/"
    fileList    = folder+"fileList.txt"
    with open(fileList,'rb') as f:
        x       = f.read().split("\n")
        user    = [u[u.rfind("/")+1:] for u in x]
        
    for fileName in x:
        with open(fileName,'rb') as f:
            user    = fileName[fileName.rfind("/")+1:]
            words   = f.read().split(" ")     
            getRandom(user,words,NUMLINES,NUMWORDS,OUTFILE)
            
    shuffle(x)
    for fileName in x:
        with open(fileName,'rb') as f:
            user    = fileName[fileName.rfind("/")+1:]
            words   = f.read().split(" ")     
            getRandom(user,words,NUMLINES,NUMWORDS,OUTFILE)

    
if __name__ == "__main__":
    main()