import copy 
import time
import math
from random import choice
N=3

def to2D(state1D): # returns 2D representation of 1D state
    return [[state1D[i+j*N] for i in range(N)] for j in range(N)]
def to1D(state2D): # returns 1D state from 2D representation
    return [item for sublist in state2D for item in sublist]

def get_children(state): # returns list of 1D state of children UDLR ordered
    state2D = to2D(state)
    idx = state.index(0)
    idx2D = divmod(idx,N)
    children=[None]*4
    if (idx2D[0]>0): 
        child2D = copy.deepcopy(state2D)
        child2D[idx2D[0]][idx2D[1]] = state2D[idx2D[0]-1][idx2D[1]]
        child2D[idx2D[0]-1][idx2D[1]] = 0
        children[0]=to1D(child2D)
    if (idx2D[0]<N-1): 
        child2D = copy.deepcopy(state2D)
        child2D[idx2D[0]][idx2D[1]] = state2D[idx2D[0]+1][idx2D[1]]
        child2D[idx2D[0]+1][idx2D[1]] = 0
        children[1]=to1D(child2D)
    if (idx2D[1]>0): 
        child2D = copy.deepcopy(state2D)
        child2D[idx2D[0]][idx2D[1]] = state2D[idx2D[0]][idx2D[1]-1]
        child2D[idx2D[0]][idx2D[1]-1] = 0
        children[2]=to1D(child2D)
    if (idx2D[1]<N-1): 
        child2D = copy.deepcopy(state2D)
        child2D[idx2D[0]][idx2D[1]] = state2D[idx2D[0]][idx2D[1]+1]
        child2D[idx2D[0]][idx2D[1]+1] = 0
        children[3]=to1D(child2D)
    return children

def get_man(state):
    state2D=to2D(state)
    dist=0
    for i in range(1,N**2):
        idx = state.index(i)
        idx2D = divmod(idx,N)
        target=divmod(i,N)
        dist=dist+abs(idx2D[0]-target[0])+abs(idx2D[1]-target[1])
    return dist
    
class State:
    def __init__(self,):
        self.loc=[0,1,2,3,4,5,6,7,8]
    def set_loc(self, new_loc):
        self.loc = new_loc #state in 1D list
    def set_parent(self, new_parent):
        self.parent = new_parent #parent of class 'state'
    def set_depth(self, new_depth): # depth of state in tree
        self.depth = new_depth
    def get_stamp(self): #returns string stamp of 'self.loc'
        return "".join(str(x) for x in self.loc)
    def get_path(self): #builds the path to this state reading 'self.parent' recursively
        st = self
        path = []
        while st.parent!=None:
            path.append(st.dir)
            st = st.parent
        return list(reversed(path))
    def set_dir(self, new_dir): #set last direction to get here, 0 to 3
        self.dir =new_dir
    def check(self): #check if solution reached
        return (list(range(N**2)) == self.loc)

def BFS(initialState):
    frontier = []
    state=State()
    state.set_loc(initialState)
    state.set_depth(0)
    state.set_parent(None)
    frontier.append(state)
#    explored = set()
    exploredstamps= set()
    exploredstamps.add(state.get_stamp())
    UDLR=["Up","Down","Left","Right"]
    max_fringe_size=0
    max_depth=0
    max_mem=0
    while not(frontier==[]): 
        max_fringe_size=max(max_fringe_size,len(frontier))
        state = frontier.pop(0)
        if (state.check()): return [[UDLR[i] for i in state.get_path()],len(state.get_path()), 
                                    len(exploredstamps)-len(frontier)-1, len(frontier), max_fringe_size, 
                                    state.depth, max_depth,time.time(),max_mem]
        for index,item in enumerate(get_children(state.loc)):
            if item!=None:
                child=State()
                child.set_loc(item)
                if not(child.get_stamp() in exploredstamps):
                    child.set_depth(state.depth+1)
                    child.set_parent(state)
                    child.set_dir(index)
                    frontier.append(child)
#                    explored.add(child)
                    exploredstamps.add(child.get_stamp())
                    max_depth=max(max_depth,child.depth)
    return False

def DFS(initialState):
    frontier = []
    state=State()
    state.set_loc(initialState)
    state.set_depth(0)
    state.set_parent(None)
    frontier.append(state)
#    explored = set()
    exploredstamps= set()
    exploredstamps.add(state.get_stamp())
    UDLR=list(reversed(["Up","Down","Left","Right"]))
    max_fringe_size=0
    max_depth=0
    max_mem=0
    while not(frontier==[]): 
        max_fringe_size=max(max_fringe_size,len(frontier))
        state = frontier.pop()
        if (state.check()): return [[UDLR[i] for i in state.get_path()],len(state.get_path()), 
                                    len(exploredstamps)-len(frontier)-1, len(frontier), max_fringe_size, 
                                    state.depth, max_depth,time.time(),max_mem]
        for index,item in enumerate(list(reversed(get_children(state.loc)))):
            if item!=None:
                child=State()
                child.set_loc(item)
                if not(child.get_stamp() in exploredstamps):
                    child.set_depth(state.depth+1)
                    child.set_parent(state)
                    child.set_dir(index)
                    frontier.append(child)
#                    explored.add(child)
                    exploredstamps.add(child.get_stamp())
                    max_depth=max(max_depth,child.depth)
    return False

def getMinCost(frontier,frontierkeys):
    mins=[i for i, x in enumerate(frontierkeys) if x == min(frontierkeys)] #get all indexes with min cost
#    print(mins)
    if (len(mins)>1):
        indexes=[]
        for i in range(4):
            for j in mins:
                if frontier[j].dir==i: indexes.append(j)
            if len(indexes)>0: return indexes[0]
            indexes=[]
    return mins[0]

def AST(initialState):
    frontier = []
    frontierkeys = []
    state=State()
    state.set_loc(initialState)
    state.set_depth(0)
    state.set_parent(None)
    frontier.append(state)
    frontierkeys.append(0)
#    explored = set()
    exploredstamps= set()
    exploredstamps.add(state.get_stamp())
    UDLR=["Up","Down","Left","Right"]
    max_fringe_size=0
    max_depth=0
    max_mem=0
    while not(frontier==[]):
        max_fringe_size=max(max_fringe_size,len(frontier))
        index=getMinCost(frontier,frontierkeys)
        state = frontier.pop(index)
        frontierkeys.pop(index)
        if (state.check()): return [[UDLR[i] for i in state.get_path()],
           len(state.get_path()), 
           len(exploredstamps)-len(frontier)-1,
           len(frontier), 
           max_fringe_size, 
           state.depth, max_depth,time.time(),max_mem]
        for index,item in enumerate(get_children(state.loc)):
            if item!=None:
                child=State()
                child.set_loc(item)
                if not(child.get_stamp() in exploredstamps):
                    child.set_depth(state.depth+1)
                    child.set_parent(state)
                    child.set_dir(index)
                    frontier.append(child)
                    frontierkeys.append(child.depth+get_man(child.loc))
#                    explored.add(child)
                    exploredstamps.add(child.get_stamp())
                    max_depth=max(max_depth,child.depth)
    return False

def IDA(initialState):
    d=0
    max_fringe_size=0
    max_depth=0
    max_mem=0
    UDLR=list(reversed(["Up","Down","Left","Right"])) 
    while(True):
        d=d+1
        frontier = []
    #    frontierkeys = []
        state=State()
        state.set_loc(initialState)
        state.set_depth(0)
        state.set_parent(None)
        frontier.append(state)
    #    frontierkeys.append(0)
    #    explored = set()
        exploredstamps= set()
        exploredstamps.add(state.get_stamp())
        while not(frontier==[]): 
            max_fringe_size=max(max_fringe_size,len(frontier))
    #        index=getMinCost(frontier,frontierkeys)
            state = frontier.pop()
    #        frontierkeys.pop(index)
            if (state.check()): return [[UDLR[i] for i in state.get_path()],len(state.get_path()), 
                                        len(exploredstamps)-len(frontier)-1, len(frontier), max_fringe_size, 
                                        state.depth, max_depth,time.time(),max_mem]
            for index,item in enumerate(list(reversed(get_children(state.loc)))):
                if item!=None:
                    child=State()
                    child.set_loc(item)
                    if (not(child.get_stamp() in exploredstamps)and((state.depth+1+get_man(child.loc))<d)):
                        child.set_depth(state.depth+1)
                        child.set_parent(state)
                        child.set_dir(index)
                        frontier.append(child)
     #                       frontierkeys.append(child.depth+get_man(child.loc))
        #                    explored.add(child)
                        exploredstamps.add(child.get_stamp())
                        max_depth=max(max_depth,child.depth)
    return False

def generate(state,NofSteps):
    steps=[]
    for i in range(NofSteps):
        possibleChildren=get_children(state.loc)
        print(state.loc)
        indexes=[i for i in range(len(possibleChildren)) if possibleChildren[i] is not None]
        chosen=choice(indexes)
        statearray=possibleChildren[chosen]
        state.set_loc(statearray)
        steps.append(chosen)
    return [state,steps]

def test(NofTimes,steps):
    a=State()
    [state,path]=generate(a,steps)
    text_file = open("output.txt", "a")
    text_file.write(str(list(reversed(path))))
    text_file.write("\n")
    text_file.close()
    solve("ida",state.loc)
    text_file = open("output.txt", "a")
    text_file.write("\n")
    text_file.close()
    

def solve(method,state):
    global N
    N=int(math.sqrt(len(state)))
    options = {"bfs" : BFS,
           "dfs" : DFS,
           "ast" : AST,
           "ida" : IDA,
    }
    baseTime=time.time()
    solved=options[method](state)
    solved[7]="{0:.8f}".format(solved[7]-baseTime)
    solved[8]="{0:.8f}".format(solved[8])
    headers=["path_to_goal: ","cost_of_path: ","nodes_expanded: ","fringe_size: ","max_fringe_size: ",
             "search_depth: ","max_search_depth: ","running_time: ","max_ram_usage: "]
    values=[]
    for i,j in zip(headers,solved):
        values.append(i+str(j))
    text_file = open("output.txt", "a")
    text_file.write("".join(str(solved)))
    text_file.close()