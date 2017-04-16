# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 20:26:43 2017

@author: TotoloM
"""
import sys
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

alpha = (0.001,0.005,0.01,0.05,0.1,0.5,1,5,10,1.1)
iterations = (100,100,100,100,100,100,100,100,100,150)

inputFile=sys.argv[1]
outputFile=sys.argv[2]
data = pd.read_csv(inputFile,names=["Age","Weight","Height"])
data_norm = (data - data.mean()) / (data.std())
data_norm["Height"]=data["Height"]
data_norm["x0"]=1
N=len(data)
for a,i in zip(alpha,iterations):
    b=np.array([0,0,0])
    outp=np.array([a,i])
    for j in range(i):
        print(j)
        b=b-a/N*np.sum(data_norm[["x0","Age","Weight"]].mul(
                np.dot(data_norm[["x0","Age","Weight"]],b)-data_norm["Height"],
                axis=0))
        print(b)          
    outp=np.append(outp,b)                  
    with open(outputFile, 'ab') as f:
        np.savetxt(f, outp[None,:], delimiter=",",fmt="%.3f")
