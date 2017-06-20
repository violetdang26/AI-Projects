#8-Piece Puzzle Solver 
#Name: HOA DANG
#UNI: hd2366
#Course: AI Summer Course

# coding: utf-8

# In[503]:

import numpy as np
from collections import deque
import time 
import resource
import heapq as pq
import sys


# In[481]:

goal = [0,1,2,3,4,5,6,7,8]


# In[482]:

def toMat(boards): #visually present the board
    boards = np.array(boards)
    if(len(boards)!=9):
        for board in boards:
            print(np.reshape(board,(3,3)))
    else:
        print(np.reshape(boards,(3,3)))


# In[483]:

def Up(node):
    child_board = node.state[:]
    i = child_board.index(0)
    child_board[i],child_board[i-3] = child_board[i-3],child_board[i]
    return(newNode(child_board,node,'Up',node.depth+1))
    
def Down(node):
    child_board = node.state[:]
    i = child_board.index(0)
    child_board[i],child_board[i+3] = child_board[i+3],child_board[i]
    return(newNode(child_board,node,'Down',node.depth+1))


def Left(node):
    child_board = node.state[:]
    i = child_board.index(0)
    child_board[i],child_board[i-1] = child_board[i-1],child_board[i]
    return(newNode(child_board,node,'Left',node.depth+1))

def Right(node):
    child_board = node.state[:]
    i = child_board.index(0)
    child_board[i],child_board[i+1] = child_board[i+1],child_board[i]
    return(newNode(child_board,node,'Right',node.depth+1))


# In[484]:

def getChildren(node): #Up Down Left Right
    
    board = node.state[:]
    pos = board.index(0)
    output=[]
    
    if(pos==0):
        output = [Down(node),Right(node)]
        
    if(pos==1):
        output = [Down(node),Left(node),Right(node)]
        
    if(pos==2):
        output = [Down(node),Left(node)]
    
    if(pos==3):
        output = [Up(node),Down(node),Right(node)]
        
    if(pos==4):
        output = [Up(node),Down(node),Left(node),Right(node)]
        
    if(pos==5):
        output = [Up(node),Down(node),Left(node)]

    if(pos==6):
        output = [Up(node),Right(node)]

    if(pos==7):
        output = [Up(node),Left(node),Right(node)]

    if(pos==8):
        output = [Up(node),Left(node)]

    return(output)


# In[485]:

def checkState(board): #print parent and child boards
    print("Parent board is (current state):")
    toMat(board)
    print("Children boards are:")
    toMat(getChildren(board))


# In[486]:

def goalTest(state):
    return(state==goal)

def getPath(node):
    path = []
    
    while(node.parent!=None):
        path.append(node.move)
        node = node.parent
    
    path = path[::-1]
    return(path)

# In[487]:

class Node:
    def __init__(self, state, parent, move,depth):
        self.state = state
        self.parent = parent
        self.move = move #direction
        self.depth = depth
        self.cost = 0
    
def newNode( state, parent, move, depth):
    return Node( state, parent, move, depth )


# In[488]:

class Frontier:
    def __init__(self):
        self.myqueue = deque()
        self.myset = set()
    
    def enqueue(self, node):
        self.myqueue.append(node)
        self.myset.add(str(node.state))
    
    def dequeue(self):
        node = self.myqueue.popleft()
        self.myset.discard(str(node.state))
        return(node)
    
    def search(self, node):
        return(str(node.state) in self.myset)
    
    def size(self):
        return(len(self.myset))

    def push(self,node):
        self.myqueue.append(node)
        self.myset.add(str(node.state))
    
    def pop(self):
        node = self.myqueue.pop()
        self.myset.discard(str(node.state))
        return(node)


# In[489]:

class Explored:
    def __init__(self):
        self.myset = set() 
    
    def add(self,node):
        self.myset.add(str(node.state))
        
    def search(self, node):
        return(str(node.state) in self.myset)
    
    def size(self):
        return(len(self.myset))


# In[490]:

def solverBFS(board):
    start = time.time()
    nodesExpanded = -1
    FrontierBFS = Frontier()
    ExploredBFS = Explored()

    root = newNode(board,None,None,0)
    FrontierBFS.enqueue(root)

    while(FrontierBFS.size()!=0):
        node = FrontierBFS.dequeue()
        nodesExpanded+=1
        ExploredBFS.add(node)


        if(goalTest(node.state)==True):
            path = getPath(node)
            break

        else:
            children = getChildren(node)
            for child in children:
                if (ExploredBFS.search(child)==False and FrontierBFS.search(child)==False):
                    FrontierBFS.enqueue(child)

    end = time.time()
    diff = end - start
    ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    writeOutput(path,nodesExpanded,node,child.depth,diff,ram)

# In[491]:

#bfs1 = [1,2,5,3,4,0,6,7,8]


# In[492]:

#solverBFS(bfs1)


# In[493]:

def solverDFS(board):
    start = time.time()
    nodesExpanded = -1
    maxDepth = 0
    FrontierDFS = Frontier()
    ExploredDFS = Explored()

    root = newNode(board,None,None,0)
    FrontierDFS.push(root)

    while(FrontierDFS.size()!=0):
        node = FrontierDFS.pop()
        nodesExpanded+=1
        ExploredDFS.add(node)


        if(goalTest(node.state)==True):
            path = getPath(node)
            break

        else:
            children = getChildren(node)[::-1]
            for child in children:
                if (ExploredDFS.search(child)==False and FrontierDFS.search(child)==False):
                    if(maxDepth<child.depth):
                        maxDepth+=1
                    FrontierDFS.push(child)
    end = time.time()
    diff = end - start
    ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    writeOutput(path,nodesExpanded,node,maxDepth,diff,ram)

# In[494]:

#solverDFS(bfs1)


# In[495]:

def hx(node): #Manhattan distance - heuristic
    board = node.state
    dist = 0
    for i in range(len(board)):
        xGoal = int(i/3)
        yGoal = i %3
        pos = board.index(i)
        xBoard = int(pos/3)
        yBoard = pos%3
        dist+=abs(xGoal-xBoard) + abs(yGoal-yBoard)
        
    return dist


# In[496]:

def gx(node):
    return(len(getPath(node)))


# In[518]:

class FrontierAStar:
    def __init__(self):
        self.myheap = []
        self.myset = set()
    
    def __getitem__(self):
        return self.myheap
    
    def insert(self,node):
        pq.heappush(self.myheap,(node.cost,node))
        self.myset.add(str(node.state))
    
    def deleteMin(self):
        _,node = pq.heappop(self.myheap)
        self.myset.discard(str(node.state))
        return(node)
    
    def size(self):
        return(len(self.myheap))
    
    def search(self, node):
        return(str(node.state) in self.myset)
    
    def getIndex(self,node):
        return(h)


# In[509]:

#board = [8,6,4,2,1,3,5,7,0]


# In[534]:

def solverAStar(board):
    start = time.time()
    nodesExpanded = -1
    maxDepth = 0
    lenF = []
    FrontierA = FrontierAStar()
    ExploredA = Explored()

    root = newNode(board,None,None,0)
    FrontierA.insert(root)

    while(FrontierA.size()!=0):
        node = FrontierA.deleteMin()
        nodesExpanded+=1
        ExploredA.add(node)


        if(goalTest(node.state)==True):
            path = getPath(node)
            break

        else:
            children = getChildren(node)[::-1]
            for child in children:
                child.cost = hx(child)+gx(child)
                if (ExploredA.search(child)==False and FrontierA.search(child)==False):
                    if(maxDepth<child.depth):
                        maxDepth+=1
                    FrontierA.insert(child)
                else:
                    for i in range(len(FrontierA.myheap)):
                        curNode = FrontierA.myheap[i]
                        if(curNode[1]==child and curNode[0]>child.cost):
                            FrontierA.myheap[i]=(child.cost,child)
                            pq.heapify(FrontierA.myheap)

    end = time.time()
    diff = end - start
    ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    writeOutput(path,nodesExpanded,node,maxDepth,diff,ram)

# In[535]:

#solverAStar([8,6,4,2,1,3,5,7,0])
def writeOutput(path,nodesExpanded,node,maxDepth,diff,ram):
    myfile = open("output.txt","w")
    
    myfile.write("path_to_goal: "+str(path)+"\n")
    myfile.write("cost_of_path: "+str(len(path))+"\n")
    myfile.write("nodes_expanded: "+str(nodesExpanded)+"\n")
    myfile.write("search_depth: "+str(node.depth)+"\n")
    myfile.write("max_search_depth: "+str(maxDepth)+"\n")
    myfile.write("running_time: "+str(diff)+"\n")
    myfile.write("max_ram_usage:"+str(ram/(1024*1024))+"\n")
    
    myfile.close()

# In[ ]:

def main():
    u_input = sys.argv
    algo = u_input[1]
    board = u_input[2].split(',')
    board = [int(i) for i in board]
    
    if(algo=='bfs'):
        print("Solving puzzle BFS method: ... ")
        solverBFS(board)
        
    if(algo=='dfs'):
        print("Solving puzzle DFS method: ... ")
        solverDFS(board)
    
    if(algo=='ast'):
        print("Solving puzzle AStar method: ... ")
        solverAStar(board)

    print("Puzzle Solved - Check output.txt for result")

main()

