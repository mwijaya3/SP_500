
# coding: utf-8

# In[73]:

import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB


# In[124]:

def crossValidation(filename):
    df=pd.read_csv(filename)
    df=df.drop([".Name", ".Symbol"], axis=1)     ##Deleting .Name and .Symbol
    
    ##Lables
    lables = np.asarray(df.columns)
    data = np.asmatrix(df)
    
    ##70-30 split, 70% train data and 30% test data
    np.random.shuffle(data)
    row, column = np.array(data).shape
    training_set_size = int(row*0.70)
    train_data = data[:training_set_size]
    test_data = data[training_set_size:]
    
    return lables, train_data, test_data

def Naive_Bayes(train, test):
    x_train = train[:,:-16]
    y_train = train[:,13]
    
    clf=GaussianNB()
    clf.fit(x_train, y_train)
    
    x_test = test[:,:-16]
    y_test = test[:,13]
    
    predict = clf.predict(x_test)
    
    rightPrediction=0
    for i in range (predict.shape[0]):
        if predict[i] == y_test[i]:
            rightPrediction+=1
    return rightPrediction      
    
if __name__ == '__main__':
    
    NumberOfIterations = 100
    totRightPre=0
    for i in range(NumberOfIterations):
        lables, train_data, test_data = crossValidation("binary-04-19-2017.csv")
        rightPrediction = Naive_Bayes(train_data, test_data)
        totRightPre+=rightPrediction
    print totRightPre/12900.0     ##12900 = NumberOfIterations*number of tests data

