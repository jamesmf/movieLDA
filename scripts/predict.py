# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 16:17:58 2015

@author: frickjm
"""

def findNearest(userNum,movie):
    with open("../data/out/nearest.txt",'rb') as f:
        lines   = f.read().split("\n")
        userNum = int(userNum) - 1
        neigh   = lines[userNum]
        print neigh
        
def main():
    findNearest(2,"154")

if __name__ == "__main__":
    main()