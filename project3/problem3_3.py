# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 20:26:43 2017

@author: TotoloM
"""
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

#import matplotlib.pyplot as plt

os.chdir("d:/Users/TotoloM/Desktop/AI/project3/")
inputFile="input3.csv"#sys.argv[1]
#outputFile=sys.argv[2]
data = pd.read_csv(inputFile)
X_train, X_test, y_train, y_test = train_test_split(data[["A","B"]],
        data["label"],stratify=data["label"],train_size=0.6)
scaler=StandardScaler().fit(X_train)

model1 = SVC(kernel='linear')
params1 = {"C": [0.1, 0.5, 1, 5, 10, 50, 100]}
gridModel1 = GridSearchCV(model1,params1,cv=5)
gridModel1.fit(scaler.transform(X_train), y_train)
print(gridModel1.score(scaler.transform(X_train),y_train))
print(gridModel1.score(scaler.transform(X_test),y_test))

model2 = SVC(kernel='poly')
params2 = {"C": [0.1, 1, 3],
           "degree": [4, 5, 6],
           "gamma": [0.1, 1.]}
gridModel2 = GridSearchCV(model2,params2,cv=5,scoring="accuracy")
gridModel2.fit(scaler.transform(X_train), y_train)
print(gridModel2.score(scaler.transform(X_train),y_train))
print(gridModel2.score(scaler.transform(X_test),y_test))

model3 = SVC(kernel='rbf')
params3 = {"C": [0.1, 0.5, 1, 5, 10, 50, 100],
           "gamma": [0.1, 0.5, 1, 3, 6, 10]}
gridModel3 = GridSearchCV(model3,params3,cv=5,scoring="accuracy")
gridModel3.fit(scaler.transform(X_train), y_train)
print(gridModel3.score(scaler.transform(X_train),y_train))
print(gridModel3.score(scaler.transform(X_test),y_test))

model4 = LogisticRegression()
params4 = {"C": [0.1, 0.5, 1, 5, 10, 50, 100]}
gridModel4 = GridSearchCV(model4,params4,cv=5,scoring="accuracy")
gridModel4.fit(scaler.transform(X_train), y_train)
print(gridModel4.score(scaler.transform(X_train),y_train))
print(gridModel4.score(scaler.transform(X_test),y_test))

model5 = KNeighborsClassifier()
params5 = {"n_neighbors" : range(1, 51),
           "leaf_size" : range(5,61,5)}
gridModel5 = GridSearchCV(model5,params5,cv=5,scoring="accuracy")
gridModel5.fit(scaler.transform(X_train), y_train)
print(gridModel5.score(scaler.transform(X_train),y_train))
print(gridModel5.score(scaler.transform(X_test),y_test))

model6 = DecisionTreeClassifier()
params6 = {"max_depth" : range(1, 51),
           "min_samples_split" : range(2,11)}
gridModel6 = GridSearchCV(model6,params6,cv=5,scoring="accuracy")
gridModel6.fit(scaler.transform(X_train), y_train)
print(gridModel6.score(scaler.transform(X_train),y_train))
print(gridModel6.score(scaler.transform(X_test),y_test))

model7 = RandomForestClassifier()
params7 = {"max_depth" : range(1, 51),
           "min_samples_split" : range(2,11)}
gridModel7 = GridSearchCV(model7,params7,cv=5,scoring="accuracy")
gridModel7.fit(scaler.transform(X_train), y_train)
print(gridModel7.score(scaler.transform(X_train),y_train))
print(gridModel7.score(scaler.transform(X_test),y_test))

                  
#with open(outputFile, 'ab') as f:
#    np.savetxt(f, outp[None,:], delimiter=",",fmt="%.3f")
