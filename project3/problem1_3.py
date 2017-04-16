# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 20:26:43 2017

@author: TotoloM
"""
import sys
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

inputFile=sys.argv[1]
outputFile=sys.argv[2]
data = pd.read_csv(inputFile,names=["feature_1","feature_2","label"])
x = np.linspace(0,16,100)
w = np.array([0,0,0]) # w1,w2,b 
data["y"] = 0
while np.sum(data["label"] != data["y"]):
#    print(np.sum(data["label"] != data["y"]))
    sampled = data[data["label"] != data["y"]].sample().index[0]
#    print(data.iloc[sampled])
    w = w + data.get_value(sampled,"label")*np.array([
            data.get_value(sampled,"feature_1"),
            data.get_value(sampled,"feature_2"),
            1])
 #   w[0] = w[0] + sampled["label"]*sampled["feature_1"]
 #   w[1] = w[1] + sampled["label"]*sampled["feature_2"]
 #   w[2] = w[2] + sampled["label"]
 #   print(w)
    if w[1]!=0:
         y = -x*w[0]/w[1]-w[2]/w[1]
#    plt.scatter(data["feature_1"],data["feature_2"],
#            c=data["label"],s=50)
#    plt.plot(x,y)
#    plt.show()
    data["y"]=np.sign(data["feature_1"]*w[0] + data["feature_2"]*w[1] + w[2])
    with open(outputFile, 'ab') as f:
        np.savetxt(f, w[None,:], delimiter=",",fmt="%d")
