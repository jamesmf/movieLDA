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
import operator
import sys


def loadThemVectors():
    outMat  = {}

    with open("vectors.txt",'rb') as f:
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
    

def main():
    vectors = loadThemVectors() #retrieve the vectors, store in dict
    king    = vectors[sys.argv[1]]   #fetch vector for king
    man     = vectors[sys.argv[2]]  #fetch vector for man
    woman   = vectors[sys.argv[3]]  #vector for woman
    queen   = vectors[sys.argv[4]]  #fetch vector for queen
    dp      = np.dot(king,man)  #dot product
    proj1   = np.multiply(man,dp)
    proj2   = np.multiply(woman,dp)
    
    print "\n\n\n"
    print getCosineDistance(np.add(np.subtract(king,proj1),proj2),vectors)
    print getCosineDistance(np.add(np.subtract(king,man),woman),vectors)
    print "\n\n\n\n"
    print getCosineDistance(np.subtract(np.subtract(king,proj1),proj1),vectors)
#    print getCosineDistance(np.subtract(king,proj1),vectors)
#    print getCosineDistance(np.subtract(king,man),vectors)
#    print "\n"
#    print getCosineDistance(np.subtract(queen,proj2),vectors)
#    print getCosineDistance(np.subtract(queen,woman),vectors)
    
if __name__ == "__main__":
    main()