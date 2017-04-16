from random import randint,choice
from BaseAI import BaseAI
import time
max_idx=1
time_limit=0.09
pruned= False
tstart=0
over=0

class PlayerAI(BaseAI):
    def __init__(self,):
        self.tstart=0
        self.over = 0
        self.phase = 0
        self.dir = 0
        self.hb = 0
        self.edge = 0
        self.pruned = False
        self.minU = 10**6
        self.maxU = -10**6
        self.adj= 0
        self.mon=0
        self.max_idx=0
        self.avcells=0
        self.maxtile=0
        self.smooth=0
    def getMove(self, grid):
 #       if (self.phase==0):
 #           self.initBoard(grid)
 #           if grid.getMaxTile()>=64: self.phase = 1
 #       else: 
        self.play(grid)
        return self.dir
    
    def get_utility(self,grid):
        self.adj=0 #FEATURE 1: N of same tiles aligned
        self.mon=0 #FEATURE 3: monotone
        self.edge=0 # FEATURE 4: large values on edges
        self.avcells=0 # FEATURE 2: N of empty cells
        self.maxtile=0 #FEATURE 5: maxtile
        self.smooth=0
        b=[] #3
        c=0 #3
        for i,x in enumerate(range(grid.size)):
            
            for j,y in enumerate(range(grid.size)):
                if (y<grid.size-1) and (x<grid.size-1):
                    b=[score_map[grid.map[x][y]],score_map[grid.map[x][y+1]],score_map[grid.map[x+1][y]]]
                    c=c + min(0,b[0]-b[1])  +  min(0,b[0]-b[2])
 #               elif (y<grid.size-1):
 #                   c=c+min(0,b[0]-b[1])
 #               elif (x<grid.size-1):
 #                   c=c+min(0,b[0]-b[2])
                
                if grid.map[x][y]>0: 
                    a=0 # 1
   #                 d= (i==0) + (j==0) #4
                    
                    if (y<grid.size-1) and (x<grid.size-1):
                        a=a+(grid.map[x][y]==grid.map[x][y+1]) + (grid.map[x][y]==grid.map[x+1][y]) # 1
   #                     b=b*(1+(grid.map[x][y]<grid.map[x][y+1]))  # 3
    #                    c=c*(1+(grid.map[y][x]<grid.map[y+1][x])) # 3
                    elif (x<grid.size-1):
                        a=a+(grid.map[x][y]==grid.map[x+1][y]) # 1
                    elif (y<grid.size-1):
                        a=a+(grid.map[x][y]==grid.map[x][y+1]) # 1
   #                     b=b*(1+(grid.map[x][y]<grid.map[x][y+1]))  # 3
   #                     c=c*(1+(grid.map[y][x]<grid.map[y+1][x])) # 3
   #                 
                    self.adj=self.adj+a#*score_map[grid.map[x][y]] # 1
  #                  self.edge=self.edge+d*score_map3[grid.map[x][y]] # 4
  #                  self.mon = self.mon + (b+c-2)*score_map[grid.map[x][y]] # 3
    #                self.maxtile=max(self.maxtile,grid.map[x][y])
                else: 
                    self.avcells=self.avcells+1 #2
        self.maxtile=score_map[self.maxtile]                                  
        #self.adj=adj2(grid)
 #       self.smooth=smooth(grid)
        self.mon=c#mon2(grid)
 #       self.adj=adjacent(grid)
        return self.avcells*3+self.adj+self.maxtile*20+self.mon*2#**2+self.mon/25#+self.edge#self.avcells*3+self.adj*1#+monotone2(state)/100#+edges(state)/100#+getmax(state)*400#+edges(state)/10#+edges(state)/5#+getmax(state)*400+monotone2(state)/3
    
    def initBoard(self,grid):
        dirs = grid.getAvailableMoves()
        if self.hb in dirs: 
            self.dir = 2*self.hb
            self.hb = not(self.hb)
        elif 1 in dirs:
            self.dir = 1
            self.hb = 0
        else:
            self.dir = 3
    def play(self,grid):
#        global tstart
#        global over
#        global max_idx
#        over= 0
        self.idx=0
        self.tstart=time.clock()
#        tstart=time.clock()
        self.over=0
        self.max_idx=1
        moves=[]
        while (time.clock()-self.tstart<time_limit):
            moves.append(self.maximize(grid,-10**6,10**6,0)[2])
            self.max_idx=self.max_idx+1
        moves=[x for x in moves if x is not None]
        if (len(moves)==1): self.dir=moves[0]
        elif len(moves)==0: self.dir=choice(grid.getAvailableMoves())
        else: self.dir=moves[-2]
            
    def minimize(self,grid,alpha,beta,idx):
        if ((time.clock()-self.tstart)>time_limit) or (idx>=self.max_idx):
            return (None,self.get_utility(grid),0)
        [minChild,minU]=[None,10**6]
        for i in grid.getAvailableCells():
            child=grid.clone()
            if randint(0,99) < 90:
                newCell=2
            else: newCell=4
#            child.setCellValue(i,choice([2,4]))
            child.setCellValue(i,newCell)
            utility=self.maximize(child,alpha,beta,idx)[1]
            if(utility<minU): 
                [minChild,minU]=[child,utility]
            if minU<=alpha: 
                return (minChild,minU,None)
            if minU < beta: beta = minU
        return (minChild,minU,None)
    def maximize(self,grid,alpha,beta,idx):
        # if self.idx>=max_idx:
        if ((time.clock()-self.tstart)>time_limit) or (idx>=self.max_idx):
            return (None,self.get_utility(grid),None)
        [maxChild,maxU]=[None,-10**6]
        move=None
        for i in grid.getAvailableMoves():
            child=grid.clone()
            child.move(i)
            utility=self.minimize(child,alpha,beta,idx+1)[1]
            if(utility>maxU):
                [maxChild,maxU,move]=[child,utility,i]
            if maxU>=beta:
                return (maxChild,maxU,move)
            if maxU > alpha: alpha = maxU    
        return (maxChild,maxU,move)
                
        
        #		moves = grid.getAvailableMoves()
#       return moves[randint(0, len(moves) - 1)] if moves else None

score_map2 = {0:0,
             2:1,
             4:2,
             8:3,
             16:5,
             32:7,
             64:10,
             128:15,
             256:22,
             512:30,
             1024:40,
             2048:1000}


score_map = {0:0,
             2:1,
             4:2,
             8:3,
             16:4,
             32:5,
             64:6,
             128:7,
             256:8,
             512:9,
             1024:10,
             2048:100,
             4096:1000,
             8192:10000,
             16384:100000}

score_map3 = {0:0,
             2:0,
             4:0,
             8:0,
             16:0,
             32:0,
             64:0,
             128:0,
             256:1,
             512:12,
             1024:12,
             2048:100}

       
def mon2(state):
    mon=0
    for x in range(state.size-1):
        for y in range(state.size-1):
            a=[score_map[state.map[x][y]],score_map[state.map[x][y+1]],score_map[state.map[x+1][y]]]
  #          mon=mon- (state.map[x][y]<state.map[x][y+1]) - (state.map[x][y]<state.map[x+1][y])
            mon=mon + min(0,a[0]-a[1])  +  min(0,a[0]-a[2])
    return mon

def matches(state,x,y,i):
    LR=0
    UD=0
    if(x+i)<state.size:
        LR=state.map[x][y]==state.map[x+i][y]*(2**(i-1))
    if(y+i)<state.size:
        UD=state.map[x][y]==state.map[x][y+i]*(2**(i-1))
    score=LR+UD
    if score>0: score=score+matches(state,x,y,i+1)#*score_map[state.map[x][y]]
    return score    
    
def smooth(state):
    score=0
    for x in range(state.size):
        for y in range(state.size):
            if state.map[x][y]!=0:
                score=score+matches(state,x,y,1)
    return score
              
def adjacent(state):
    mul=2
    adj=0
    for x in range(state.size-1):
        for y in range(state.size-1):
            if state.map[x][y]>0:
                a=score_map[state.map[x][y]]
                if (x<(state.size-2)) and (y<(state.size-2)):
                    adj=adj+a*(( state.map[x][y]==state.map[x+1][y])*(1+(state.map[x][y]*2==state.map[x+1][y+1])*mul+(state.map[x][y]*2==state.map[x+2][y])*mul+(state.map[x][y]*2==state.map[x][y+2])*mul))
                if (x<(state.size-2)):    
                    adj=adj+a*(( state.map[x][y]==state.map[x+1][y])*(1+(state.map[x][y]*2==state.map[x+1][y+1])*mul+(state.map[x][y]*2==state.map[x+2][y])*mul))
                if (y<(state.size-2)):    
                    adj=adj+a*(( state.map[x][y]==state.map[x+1][y])*(1+(state.map[x][y]*2==state.map[x+1][y+1])*mul+(state.map[x][y]*2==state.map[x][y+2])*mul))
                else:    
                    adj=adj+a*(( state.map[x][y]==state.map[x+1][y])*(1+(state.map[x][y]*2==state.map[x+1][y+1])*mul))
        if state.map[x][y]>0:
            adj=adj+((state.map[state.size-1][x]==state.map[state.size-1][x+1]) +(state.map[x][state.size-1]==state.map[x+1][state.size-1]))            
    return adj

def adj2(state):
    adj=0
    for x in range(state.size):
        for y in range(state.size):
            if state.map[x][y]>0:
                a=0
                if (y<state.size-1) and (x<state.size-1):
                    a=a+(state.map[x][y]==state.map[x][y+1]) + (state.map[x][y]==state.map[x+1][y])
                elif (x<state.size-1):
                    a=a+(state.map[x][y]==state.map[x+1][y])
                elif (y<state.size-1):
                    a=a+(state.map[x][y]==state.map[x][y+1])
                adj=adj+a#*score_map[state.map[x][y]]    
    return adj
    
def edges(state):
    adj=0
    for i,x in enumerate(range(state.size)):
        for j,y in enumerate(range(state.size)):
            score = (i==0) + (j==0) #+ (i==(state.size-1))  + (j==(state.size-1))
            if score>0:
                adj=adj+score_map3[state.map[x][y]]*score
    return adj


def monotone(state):
    mon=0
    for x in range(state.size-1):
        for y in range(state.size-1):
            a=score_map2[state.map[x][y]]
            b=score_map2[state.map[x][y+1]]
            c=score_map2[state.map[x+1][y]]
            d=score_map2[state.map[x+1][y+1]]
            mon=mon+max(0,a-b)+max(0,a-c)+max(0,a-b)*max(0,a-c)*2+max(0,a-d)
    #            mon=mon+3*a-b-c-d+(a-b)*(a-c)
        mon=mon+max(0,score_map2[state.map[state.size-1][x]]-score_map2[state.map[state.size-1][x+1]])+max(0,score_map2[state.map[state.size-1][x]]-score_map2[state.map[state.size-1][x+1]])    
    return mon



def monotone2(state):
    mon=0
    for x in range(state.size):
        a=1
        b=1
#        c=1
        for y in range(state.size-1):
 #            a=a*state.map[x][y]>state.map[x][y+1]
 #            b=b*state.map[y][x]>state.map[y+1][x]
             a=a*(1+(state.map[x][y]<state.map[x][y+1]))
             b=b*(1+(state.map[y][x]<state.map[y+1][x]))
#        if (x<state.size-1):
#             c=c*(1+(state.map[x][y]<state.map[x+1][y+1]))
        mon=mon+(a+b-2)*score_map2[state.map[x][y]]
    return mon


def monadj(state):
    val=0
    z=len(state.getAvailableCells())>0
    for x in range(state.size-1):
        for y in range(state.size-1):
            if state.map[x][y]>0:
                a=score_map[state.map[x][y]]
                b=score_map[state.map[x][y+1]]
                c=score_map[state.map[x+1][y]]
                d=score_map[state.map[x+1][y+1]]
                val=val+z*((state.map[x][y]==state.map[x][y+1])+(state.map[x][y]==state.map[x+1][y]))*a+(max(0,a-b)+max(0,a-c)+max(0,a-d))*1.5
    return val  

def getmax(state):
    maxTile=0 
    for x in range(state.size):
            for y in range(state.size):
                if state.map[x][y]>maxTile: indexes=[x,y]
                maxTile = max(maxTile, state.map[x][y])
    return indexes==[0,0]
          
def get_utility(state):
    avcells=len(state.getAvailableCells())
    return avcells*3+adj2(state)*1#+monotone2(state)/100#+edges(state)/100#+getmax(state)*400#+edges(state)/10#+edges(state)/5#+getmax(state)*400+monotone2(state)/3
 #   return len(state.getAvailableCells())*3+monadj(state)*2
 #   return len(state.getAvailableCells())*3+(len(state.getAvailableCells())>0)*adjacent(state)*2-monotone(state)*5#+(state.getMaxTile()==1024)*10+(state.getMaxTile()==2048)*10
               
def minimize(state,alpha,beta,idx):
    global pruned
    global minU
    global over
    if len(state.getAvailableMoves())==0: return (None,get_utility(state),None)
    if (time.clock()-tstart)>time_limit: 
#        over=1
        return (None,get_utility(state),0)
    if idx>=max_idx:
#    if time.clock()-idx>time_limit:
        return (None,get_utility(state),None)
    [minChild,minUtility]=[None,10**6]
    for i in state.getAvailableCells():
        child=state.clone()
        child.setCellValue(i,choice([2,4]))
        utility=maximize(child,alpha,beta,idx)[1]
        if(utility<minUtility): [minChild,minUtility]=[child,utility]
        if minUtility<=alpha: 
            pruned = True
            return (minChild,minUtility,None)
        if minUtility < beta: beta = minUtility
#        if over: return (minChild, minUtility,None)
    minU=minUtility
    return (minChild,minUtility,None)

def maximize(state,alpha,beta,idx):
    global pruned
    global maxU
    global over
    if len(state.getAvailableMoves())==0: return (None,get_utility(state),None)
    if (time.clock()-tstart)>time_limit: 
 #      print("time out")
       return (None,get_utility(state),None)
    if idx>=max_idx:
#    if time.clock()-idx>time_limit:
        return (None,get_utility(state),None)
    [maxChild,maxUtility]=[None,-10**6]
    move=None
    for i in state.getAvailableMoves():
        child=state.clone()
        child.move(i)
        utility=minimize(child,alpha,beta,idx+1)[1]
        if(utility>maxUtility): [maxChild,maxUtility,move]=[child,utility,i]
        if maxUtility>=beta: 
            pruned = True
            return (maxChild,maxUtility,move)
        if maxUtility > alpha: alpha = maxUtility
#        if over: 
#            return (maxChild, maxUtility,move)
    maxU=maxUtility
    return (maxChild,maxUtility,move)

    
         