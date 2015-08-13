from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.advanced_activations import PReLU, LeakyReLU
from keras.layers.recurrent import SimpleRNN, SimpleDeepRNN
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU

import pandas as pd
import numpy as np 
from sklearn import preprocessing


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
    
def getTestSet(testLoc):
    with open(testLoc,'rb') as f:
        return f.read().split("\n")
        
def getTrainSet(trainLoc):
    with open(trainLoc,'rb') as f:
        return f.read().split("\n")
        
        

def ratingsToData(ratings,vectors):
    X   = []
    y   = []
    for line in ratings:
        r   = [0,0,0,0,0]
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


def main():
    np.random.seed(1919)
    
    ### Constants ###
    data_folder = "../data/"
    out_folder = "../data/out/"
    batch_size = 4
    nb_epoch = 10
    
    ### load train and test ###
    
    
    
    train  = pd.read_csv(data_folder+'train.csv', index_col=0)
    test  = pd.read_csv(data_folder+'test.csv', index_col=0)
    print "Data Read complete"
    
    Y = train.Survived
    train.drop('Survived', axis=1, inplace=True)
    
    columns = train.columns
    test_ind = test.index
    
    train['Age'] = train['Age'].fillna(train['Age'].mean())
    test['Age'] = test['Age'].fillna(test['Age'].mean())
    train['Fare'] = train['Fare'].fillna(train['Fare'].mean())
    test['Fare'] = test['Fare'].fillna(test['Fare'].mean())
    
    category_index = [0,1,2,4,5,6,8,9]
    for i in category_index:
        print str(i)+" : "+columns[i]
        train[columns[i]] = train[columns[i]].fillna('missing')
        test[columns[i]] = test[columns[i]].fillna('missing')
    
    train = np.array(train)
    test = np.array(test)
       
    ### label encode the categorical variables ###
    for i in category_index:
        print str(i)+" : "+str(columns[i])
        lbl = preprocessing.LabelEncoder()
        lbl.fit(list(train[:,i]) + list(test[:,i]))
        train[:,i] = lbl.transform(train[:,i])
        test[:,i] = lbl.transform(test[:,i])
    
    ### making data as numpy float ###
    train = train.astype(np.float32)
    test = test.astype(np.float32)
    #Y = np.array(Y).astype(np.int32)
    
    model = Sequential()
    model.add(Dense(len(columns), 512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(512, 1))
    model.add(Activation('softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer="adam")
    model.fit(train, Y, nb_epoch=nb_epoch, batch_size=batch_size, validation_split=0.20)
    preds = model.predict(test,batch_size=batch_size)
    
    pred_arr = []
    for pred in preds:
        pred_arr.append(pred[0])
    
    ### Output Results ###
    preds = pd.DataFrame({"PassengerId": test_ind, "Survived": pred_arr})
    preds = preds.set_index('PassengerId')
    preds.to_csv(out_folder+'test.csv')
