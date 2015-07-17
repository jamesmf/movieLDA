# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:06:41 2015

@author: James Frick

NIH Center for Advancing Translational Sciences
jamesmfrick@gmail.com

Most of the supporting functions for dictionary creation, preprocessing, and scoring
"""
import numpy as np
import cPickle
import operator
from nltk.corpus import stopwords
from nltk.stem  import porter
import re
import enchant
import operator
import sys
import scipy.stats as sts
from scipy.spatial.distance import euclidean

#reads in a dictionary file that is output by createdict.py, adds ID string
def read_dict(filename):
    f       =   open(filename).readlines()
    count   = 0
    diction = {}
    for line in f:
        line = line.replace("\n",'')
        diction[line]   = count
        count+=1
    return diction
    
#read records from the the omim text file
def read_omim_recs(filename):
    mystr       = open(filename).read()
    doc_list    = []
    i2          = 0
    while i2 > -1:
        i1 = mystr.find("*RECORD",i2)
        try:    
            i2 = mystr.find("*RECORD",i1+1)
            rec= mystr[i1:i2]
            doc_list.append(rec)
        except ValueError as err:
            print err
            i2 = -1
    return doc_list
    
def read_in_wiki_pickle(pickleString):
    with open(pickleString,'rb') as titleP:
        wikiDocs    =   cPickle.load(titleP)
    return wikiDocs



def read_topic_dist(gammaPickle):

    with open(gammaPickle,'rb') as gammaP:
        docTopics   =   cPickle.load(gammaP)

    return docTopics

def getAncestorMap(omim,d2d):
    pass

###############################################################################
#SIMILARITY FUNCTIONS    
###############################################################################

    
def find_index(nameString,docNames):
    nameString = nameString.lower()
    print nameString
    count=0
    for i in docNames:
        i = i.lower()
        if i.find(nameString) > -1:
            print i, count
            yn  = str(raw_input("Is this the record you'd like to match? (y/n)\n").lower())
            if yn == "y":
                return count
        count+=1        
    return -1
    
def findMultIndex(allsearch,docNames):
    indices =   []
    for i in range(0,len(allsearch)):
        indices.append(find_index(allsearch[i],docNames))
    return indices
            
def get_sim_docs(docIndex,docTopics,KL=None):
    if type(docIndex) is int:
            docIndex=[docIndex]

    vec1    =   np.zeros(docTopics[0].shape)
    for i in range(0,len(docIndex)):  
        vec1    =   np.add(vec1,docTopics[docIndex[i]])
    scores  =   []

    l   =   len(docTopics)

    for i in range(0,l):
        if i not in docIndex:
            vec2    =   np.array(docTopics[i],dtype=np.float)

            scores.append(-sts.entropy(vec1,vec2))
        else:
            scores.append(99999999)

    count=0
    names   = {}
    for x in scores:
        user   = 'user_'+str(count + 1) #REMEMBER USERS ARE INDEXED STARTING AT 1
        names[user]    =   x
        count+=1
    nl= sorted(names.items(),key=operator.itemgetter(1),reverse=True)
    return nl


       

        
    
###############################################################################
#PREPROCESSING FUNCTIONS    
###############################################################################
def get_dictionary(docs, dictFilters=None):
    #dictFilters = None
    dicts = []
    allwords = set()
    for doc in docs:
        allwords = allwords | set(doc.keys())
    if dictFilters:
        for filter in dictFilters:
            allwords = filter(allwords, dicts)
    dict_list = list()
    index_map = {}
    i = 0
    for word in allwords:
        dict_list.append(word)
        index_map[word] = i
        i += 1

    return dict_list, index_map

def write_dictionary(dict_list,totalwords, path="../data/dictionary.txt"):
    count=0
    tag = "_" + str(int(totalwords/1000))+"k.txt"
    path.replace(".txt",tag)
    with open(path, "w") as f:
        for word in dict_list:
            if count < totalwords:
                f.write(word + "\n")
                count+=1
                
def write_stem_mapping(stemmed):
    with open("../data/stemmed_mapping.txt",'wb') as f:
        for k,v in stemmed.iteritems():
            f.write(k+"\t"+v+"\n")
            
    


def plaintext_to_wordcounts(words,cutoff):

    counts  = {}
    #stemmer = nltk.stem.porter.PorterStemmer()
    ret_dict= {}
    for word in words:
        #word   = stemmer.stem(word)
        try:
            counts[word] += 1
        except KeyError:
            counts[word] = 1
    ret = sorted(counts.items(),key=operator.itemgetter(1),reverse=True)
    with open("../data/dictCounts.txt",'wb') as f:
        for i in range(0,cutoff):
            try:
                ret_dict[ret[i][0]] = ret[i][1]
                f.write(str(ret[i][0])+"\t"+str(ret[i][1])+"\n")
            except:
                pass
    return ret_dict

def file_list_to_lda(whole_str, cutoff, stop=None, stem=None):
    ignore  =   []
                
    docs = []
    if stop:
        stops   =   stopwords.words("english")
    engDict = enchant.Dict("en_US")
    stemmer = porter.PorterStemmer()
    no_nums = re.compile("[0-9]+")
    noa1    = re.compile("[a-zA-Z][0-9]")
    words = re.findall("[a-zA-Z0-9_]+", whole_str)
    print len(words)
    words = [word for word in words if (word not in stops) & (word not in ignore) &(len(word) > 2)]
    print len(words)
    words   =[word for word in words if not (re.match(no_nums,word) or re.match(noa1,word))]
    print len(words)
    stemmed_dict={}
    for i in range(0,len(words)):
        w   =   words[i]
        if engDict.check(w):
            if stem:
                words[i]= stemmer.stem(w)
            try:            
                st      = stemmed_dict[words[i]]            
                if st.find(w) < 0:
                    stemmed_dict[words[i]]=st+","+w
            except KeyError:
                stemmed_dict[words[i]]=w
    doc = plaintext_to_wordcounts(words,cutoff)
    docs.append(doc)
    # 'docs' is a list of lists of words that have been pre-processed
    dict_list, index_map = get_dictionary(docs)
    write_dictionary(dict_list,cutoff)
    write_stem_mapping(stemmed_dict)
    return 
    
def stem_docs(docs):
    c=re.compile("[\[\]\(\)\]!,.=\-;']")
    stemmer =   porter.PorterStemmer()
    engDict =   enchant.Dict("en_US")
    alphan = re.compile("^[a-zA-Z0-9]+")
    count=0
    for x in docs:
        x = re.sub(c,' ',x)
        x2  = ""
        ws  =   re.split("\s+",x)
        for w in ws:
            if not w == '':
                try:
                    if not re.match(alphan,w):
                        pass
                    else:
                        if engDict.check(w):
                            w2  =   stemmer.stem(w)
                            x2  += " "+w2
                        else:
                            x2  += " "+w
                except UnicodeDecodeError:
                    pass
        docs[count] = x2
        count+=1
    return docs

            
    
    