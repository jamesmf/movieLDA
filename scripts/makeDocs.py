# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 19:51:39 2015

@author: jmf
"""

import sys
from os import listdir

def main():
    makeDocuments("../data/raw/")
    
def writeDoc(fields,rating):
    idx = int(fields[2]) - 1
    if int(fields[2]) > 3:
        out = ("like_"+fields[1]+" ",rating[idx])
    elif int(fields[2]) < 3:
        out = ("dislike_"+fields[1]+" ",rating[idx])
    else:
        out = ("",0)
    return out
    
    
def makeDocuments(inFolder):
    rating  = [3,1,0,1,3]
    files   = listdir(inFolder+"base/")
    for fi in files:
        with open(inFolder+"base/"+fi,'rb') as f:
            lines   = f.read().split("\n")
        for line in lines:
            fields  = line.split("\t")
            if len(fields) > 1:
                with open(inFolder+"../processed/item_"+fields[0]+".txt",'a') as f2:
                    out = writeDoc(fields,rating)
                    for i in range(0,out[1]):
                        f2.write(out[0])    
    
if __name__ == "__main__":
    main()