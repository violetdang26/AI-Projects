from random import randint
from BaseAI import BaseAI
import math
import time
import numpy as np


class PlayerAI(BaseAI):
	def __init__(self):
		self.prevTime = 0

	def getMove(self, grid):

		self.prevTime = time.clock()
		depth = 3
		node = Node(grid)

		(child, _) = self.maximize(node, float('-Inf'), float('Inf'), depth)

		return(child.move)

	def minimize(self,node,alpha,beta,depth):

		children = self.getChildren(node,max=True) #

		if(self.isOver(children) or depth == 0): #t
			return((None,evaluate(node)))	

		(minChild,minUtility) = (None,float('inf'))		

		for child in children:

			(_,utility) = self.maximize(child,alpha,beta,depth-1)
			if(utility < minUtility):
				(minChild, minUtility) = (child, utility)

			if(minUtility <= alpha):
				break

			if(minUtility < beta):
				beta = minUtility

		return (minChild, minUtility)

	def maximize(self,node,alpha,beta,depth):

		children = self.getChildren(node,max=True)
		
		if(self.isOver(children) or depth == 0): #time.clock()-self.prevTime>.2 or 
			return((None,evaluate(node)))	

		(maxChild, maxUtility) = (None, float('-Inf'))

		for child in children:
			(_, utility) = self.minimize(child, alpha, beta, depth-1)

			if(utility > maxUtility):
				(maxChild, maxUtility) = (child, utility)

			if(maxUtility >= beta):
				break

			if(maxUtility > alpha):
				alpha = maxUtility

		return (maxChild, maxUtility)
	

	def getChildren(self,node,max):
		grid = node.grid
		children = []

		if max:
			moves = grid.getAvailableMoves()
			for m in moves:
				myGrid = grid.clone()
				myGrid.move(m)
				newNode = Node(myGrid,m)
				children.append(newNode)

		else:
			opencells = grid.getAvailableCells()
			if not (isBoardfull(opencells)):
				for cell in opencells:
					for val in [2,4]:
						myGrid = grid.clone()
						myGrid.setCellValue(cell,val)
						newNode = Node(myGrid,None)
						children.append(newNode)

		children.sort(key=evaluate)			

		return(children)

	def isOver(self,children):
		if(len(children)) == 0:
			isOver=True

	def isBoardfull(self, opencells):
		return(len(opencells)==0)

class Node():
	def __init__(self,grid,move=None):
		self.grid = grid
		self.move = move
		#self.util = None

def maxTileCorn(node):
	maxTile = node.grid.getMaxTile()
	istrue = node.grid.map[3][3]==maxTile
	return 1 if istrue else 0
 

def monotonic(grid):
	w = .5
	i=0
	w1=0
	w2=0
	l = [3,2,1,0]
	for x in xrange(3,-1,-1):
	    for y in xrange(0,4):
	        if(x==2 or x==0):
	            y=l[y]
	        w1+= grid.map[x][y]*pow(w,i)
	        i+=1


	i = 0 
	for y in xrange(0,4,1):
	    for x in xrange(0,4,1):
	    #for x in range(3,-1,-1):
	    	if(y==2 or y==0):
	        	x=l[x]
	        w2+= grid.map[x][y]*pow(w,i)
	        i+=1

	return(max(w1,w2))


def smoothness(grid): #minimize this count
	diff = 0

	diff += abs(grid.map[0][0]-grid.map[0][1]) + abs(grid.map[0][1]-grid.map[0][2]) + abs(grid.map[0][2]-grid.map[0][3])
	diff += abs(grid.map[1][0]-grid.map[1][1]) + abs(grid.map[1][1]-grid.map[1][2]) + abs(grid.map[1][2]-grid.map[1][3])
	diff += abs(grid.map[2][0]-grid.map[2][1]) + abs(grid.map[2][1]-grid.map[2][2]) + abs(grid.map[2][2]-grid.map[2][3])
	diff += abs(grid.map[3][0]-grid.map[3][1]) + abs(grid.map[3][1]-grid.map[3][2]) + abs(grid.map[3][2]-grid.map[3][3])

	diff += abs(grid.map[0][0]-grid.map[1][0]) + abs(grid.map[1][0]-grid.map[2][0]) + abs(grid.map[2][0]-grid.map[3][0])
	diff += abs(grid.map[0][1]-grid.map[1][1]) + abs(grid.map[1][1]-grid.map[2][1]) + abs(grid.map[2][1]-grid.map[3][1])
	diff += abs(grid.map[0][2]-grid.map[2][1]) + abs(grid.map[1][2]-grid.map[2][2]) + abs(grid.map[2][2]-grid.map[3][2])
	diff += abs(grid.map[0][3]-grid.map[3][1]) + abs(grid.map[1][3]-grid.map[3][3]) + abs(grid.map[2][3]-grid.map[3][3])

	return(math.log(diff,2))


def countMerger(grid):
	total = 0
	l = []
	for x in xrange(0,3):
		for y in xrange(0,3):
			if grid.map[x][y]!=0:
				l.append(grid.map[x][y])
		if(len(l)>0):
			for i in xrange(len(l)-1):
				if l[i]==l[i+1]:
					total+=1

	for y in xrange(0,3):
		for x in xrange(0,3):
			if grid.map[x][y]!=0:
				l.append(grid.map[x][y])

		if(len(l)>0):
			for i in xrange(len(l)-1):
				if l[i]==l[i+1]:
					total+=1

	return total


def evaluate(node):
	grid = node.grid
	#best combo 2,-2,10,3,1: 512,512,256,
	#snake 12 good too

	#8, -4, 10 ,5,2 : 1024, 256, 
	#merger 3 512--128
	wopen = 8
	wsmooth = -4
	wmonotonic = 10
	wcorner = 5
	wmax = 2
	wmerger = 2

	maxTile = grid.getMaxTile()
	cornerTile = maxTileCorn(node)
	opencells = len(grid.getAvailableCells())
	smooth = smoothness(grid)
	monoton = monotonic(grid)
	mergers = countMerger(grid)

	return wmonotonic*monoton + wopen*opencells+ wmax*math.log(maxTile,2) +wsmooth*smooth + wcorner*cornerTile + wmerger*mergers # + total

