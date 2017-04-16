# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 08:29:53 2017

@author: TotoloM
"""
def createSudoku(start):
    sdk = {}
    cols = range(1,10)
    rows = ("A","B","C","D","E","F","G","H","I")
    index = 0
    for i in rows:
        for j in cols:
            if start[index]=="0":
                sdk[i + str(j)] = list(map(str,list(range(1,10))))
            else: 
                sdk[i + str(j)] = [start[index]]
            index += 1
    return sdk
    
def printSudoku(sudoku):
    string=""
    cols = range(1,10)
    rows = ("A","B","C","D","E","F","G","H","I")
    index = 0
    for i in rows:
        for j in cols:
            if len(sudoku[i + str(j)]) == 0:
                return False
            elif len(sudoku[i + str(j)]) > 1:
                string += "0"
            else:
                string += str(sudoku[i + str(j)][0])
            index += 1
    for i in range(9):
        print(" ".join(string[i*9:i*9+3])+"|"+
              " ".join(string[i*9+3:i*9+6]) + "|"+
              " ".join(string[i*9+6:i*9+9]))
        if i==2 or i==5: print("-----------------")

def buildString(sudoku):
    string = ""
    cols = range(1,10)
    rows = ("A","B","C","D","E","F","G","H","I")
    index = 0
    for i in rows:
        for j in cols:
            if len(sudoku[i + str(j)]) == 0:
                return False
            elif len(sudoku[i + str(j)]) > 1:
                string += "0"
            else:
                string += str(sudoku[i + str(j)][0])
            index += 1
    return string

def checkSudoku(sudoku):
    cols = range(1,10)
    rows = ("A","B","C","D","E","F","G","H","I")
    index = 0
    for i in rows:
        for j in cols:
            if len(sudoku[i + str(j)]) != 1:
                return False
                index += 1
    return True

def getNeighbours(cell):
    pool = set()
    cols = range(1,10)
    rows = ("A","B","C","D","E","F","G","H","I")
    row = cell[0]
    col = cell[1]
    for i in cols:
        pool.add(row + str(i))
    for i in rows:
        pool.add(i + col)
    if int(col)<4: 
        colgroup=["1","2","3"]
    elif int(col)<7: 
        colgroup=["4","5","6"]
    else: 
        colgroup=["7","8","9"]
    if row in ["A","B","C"]:
        rowgroup=["A","B","C"]
    if row in ["D","E","F"]:
        rowgroup=["D","E","F"]
    if row in ["G","H","I"]:
        rowgroup=["G","H","I"]
    for i in colgroup:
        for j in rowgroup:
            pool.add(j + i)
    pool.remove(cell)
    return pool

def getAllArcs():
    pool= set()
    cols = range(1,10)
    rows = ("A","B","C","D","E","F","G","H","I")
    pair=[]
    for i in rows:
        for j in cols:
            for k in getNeighbours(i + str(j)):
                pair = [i + str(j)]
                pair.append(k)
#                pair.sort()
                pool.add("".join(pair))
    return pool

def Revise(sudoku, cell1, cell2):
    revised = False
    for i in sudoku[cell1]:
        if sudoku[cell2]==[i]:
            sudoku[cell1].remove(i)
            revised = True
    return [revised, sudoku]

def AC3(sudoku_start):
    sudoku = createSudoku(sudoku_start)
    queue = getAllArcs()
    while len(queue):
        arc=queue.pop()
        cell1=arc[:2]
        cell2=arc[2:]
        revised, sudoku = Revise(sudoku, cell1, cell2)
        if revised:
            if len(sudoku[cell1]) == 0:
                return [False, sudoku]
            for i in getNeighbours(cell1):
                if i != cell2:
                    pair = [i,cell1]
#                    pair.sort()
                    queue.add("".join(pair))
    return [True, sudoku]
    
def Backtrack(assignment):
#    print(buildString(assignment))
    if checkSudoku(assignment):
#        print("OK")
        return assignment
    cell=""
    l=10
    while(True):
        for i,j in assignment.items():
            if (len(j)<l) and (len(j)>1):
                l=len(j)
                cell=i
#        print(cell,assignment[cell])
        if assignment[cell]==[]:
#            print("??")
            return assignment
        for i in assignment[cell]:
            new_assignment=assignment.copy()
            new_assignment[cell]=[i]
#            print(i)
#            print(buildString(new_assignment))
            noError, result = AC3(buildString(new_assignment))
            if noError:
                result = Backtrack(result)
            if checkSudoku(result):
                return result
            assignment[cell].remove(i)
    return assignment
        
        
    
            
    
    
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        