# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 11:51:41 2017

@author: TotoloM
"""

import GameManager_3
a=[]
while(True):
    a.append(GameManager_3.main())
    text_file = open("output.txt", "a")
    text_file.write(str(a)+"\n")
    text_file.close()