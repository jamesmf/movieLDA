# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 14:14:50 2015

@author: frickjm
"""



#sys.path.reverse()
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
import matplotlib.pyplot as pl
from scipy.spatial import distance 
from scipy.stats import entropy
import operator
import sys


def loadThemVectors():
    outMat  = {}

    with open("../data/out/vectors.txt",'rb') as f:
        for line in f.readlines():
            sp  = line.split()
            name= sp[0].strip()
            
            arr     = np.array(sp[1].split(","))
            arr     = [float(x) for x in arr]

            outMat[name]    = arr
            
    return outMat
    



def getCosineDistance(v1,vectorz):
    sims    = {}
    for k,v in vectorz.iteritems():
        sims[k]     = distance.cosine(v1,v)
    out     = sorted(sims.items(), key=operator.itemgetter(1))[:12]
    return out
    

def predict(test,vectors):
    tot = 0
    for line in test:
        sp  = line.split("\t")
        if len(sp) > 1:
            user= sp[0]
            mv  = sp[1]
            rtg = sp[2]
            userword    = "user_"+user.strip()+".txt"
            likeword    = "like_"+mv
            dislword    = "dislike_"+mv
            uservec     = vectors[userword]
            likevec     = vectors[likeword]
            disvec      = vectors[dislword]
            likeCos     = distance.cosine(uservec,likevec)
            disCos      = distance.cosine(uservec,disvec)
            likeKL      = entropy(uservec,likevec)
            disKL       = entropy(uservec,disvec)
            print userword, likeword, dislword
            print rtg, likeCos, disCos
            print rtg, likeKL, disKL
            stop = raw_input("woot")
            
def getTestSet(testLoc):
    with open(testLoc,'rb') as f:
        return f.read().split("\n")


def main():
    testSet = getTestSet("../data/raw/test/ua.test")
    vectors = loadThemVectors() #retrieve the vectors, store in dict
    predict(testSet,vectors)
    
if __name__ == "__main__":
    main()