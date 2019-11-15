# A simple Python3 program that returns the index of a move our agent should make
#(range: [1,7])
#MM is a backtracking based algorithm, for each possible current move it looks
#ahead a certain number of turns (treeDepth) then backtracks and makes a well informed
#move. (DFS)

#an alternative would be to create one big tree that is used to inform multiple
#consecutive moves. But a big tree like that  would require storing.

#note: nodeindex always represents the position in the current level

import math
from sys import maxsize
import numpy as np

def minimax (curDepth, nodeIndex,
			maxTurn, scores,
			targetDepth,branchFactor,currentBoardState, moveIndex):
    #DEBUG:this represents the depth
	print("D"+str(curDepth)+": ")

	# base case : targetDepth (max depth) reached
	if (curDepth == targetDepth):
		#DEBUG:Leaf index and value
		#print("LEAF node no."+str(nodeIndex) +" value: "+ str(scores[nodeIndex]))
        #use the state that has been passed down to compute value


		print("Board state after move: "+str(moveIndex + 1) + ":")
		#Board changer, takes a Board.board 2d array, a move index
		#and returns the next board.
		nextB = nextBoard(maxTurn, currentBoardState, moveIndex)
		print(str(nextB))
		score = evaluateBoard(nextB)
		scores[nodeIndex] = score
		#BoardEvaluator
		return scores[nodeIndex]

	if (maxTurn):
		#for storing the child valuations
		moves = [0]*branchFactor

		print("Boardstate passed to leaves:")
		print(currentBoardState)
		print('\n')
		#Run minimax on each child (future turns)
		for moveIndex in range (0,branchFactor):
			print("Start MM")
			moves[moveIndex] = minimax(curDepth + 1,
			nodeIndex * branchFactor + moveIndex ,False, scores, targetDepth
			, branchFactor, currentBoardState,moveIndex)
			print("End MM\n")
		moveIndex = 0
        #find max child value
		bestValue = max(moves)

        #print the result of every max node evaluation
		print("D"+str(curDepth)+": "+"MAX node no."+str(nodeIndex) +
			" value: "+ str(bestValue))

		#Print move based on minimax value if we're back at the present turn
		#this will be the index of the child with best
		if (curDepth == 0):
			print("\nYou should MOVE "+str(moves.index(max(moves))+1))

		#return max child value to parent
		return bestValue

	else:
		#for storing the child valuations
		moves = [0]*branchFactor

		#Run minimax on each child (future turns)
		for moveIndex in range(0,branchFactor):
			moves[moveIndex] = minimax(curDepth + 1, nodeIndex * branchFactor + moveIndex
			,True, scores, targetDepth,branchFactor, currentBoardState,moveIndex)
		moveIndex = 0
		#find min child value
		bestValue = min(moves)

        #print the result of every min node evaluation
		print("D"+str(curDepth)+": "+"MIN node no."+str(nodeIndex) +
			" value: "+ str(bestValue))

		#Print move based on minimax value if we're back at the present turn
		#this will be the index of the child with best value
		if (curDepth == 0):
			print("MOVE "+str(moves.index(min(moves))+1))

	    #return min child value to parent
		return bestValue

def nextBoard(lastTurnWasMax, currentBoardState, moveIndex):
	curBoardState = currentBoardState.copy()
	if (lastTurnWasMax):
		startPit = moveIndex
		skipScoreOne = False
		skipScoreTwo = True
	else:
		startPit = moveIndex + 8
		skipScoreOne = True #must skip first pit when sowing
		skipScoreTwo = False
	#collect the seeds, emptying the pit
	seedStash = curBoardState[startPit]
	curBoardState[startPit] = 0
	curPit = startPit
	#sow the seeds anti-clockwise
	while seedStash > 0:
		#move to next curpit
		if (curPit == 15):
			curPit = 0 #end of array was reached, reset
		else:
			curPit +=1
		if not((skipScoreOne and curPit == 7) or(skipScoreTwo and curPit == 15) ):
			curBoardState[curPit]+=1
			seedStash-=1
	return curBoardState

def evaluateBoard(boardState):

	#treat pieces on a side as equivalent to being in that side's score
	seedsOnMaxSide = sum(boardState[8:15])
	seedsOnMinSide = sum(boardState[0:7])

	score = seedsOnMaxSide - seedsOnMinSide
	#south - north
	return score


startDepth = 0
firstLeafIndex = 0

#South is maximising player, set to 1 to run as Norths
isMaxPlayer = 0
branchFactor = 7

# Creates a list containing 5 lists, each of 8 items, all set to 0
columns = 16;
initialBoardState = [0 for x in range(columns)]
for col in range (0,8):
	initialBoardState[col] = 7
	initialBoardState[col+8] = 7
initialBoardState[7] = 0
initialBoardState[15] = 0
# heuristic calculations at leaves
treeDepth = 1 #2:Agent moves once, trying to minimize the damage opp will make
              #on its next move
totalNoOfLeaves = branchFactor ** treeDepth
scores = [0]* totalNoOfLeaves
moveIndex = 0

#scores = np.random.randint(-98,98, totalNoOfLeaves)


#DEBUG:
treeDepthCheck = math.log(len(scores), branchFactor)
print("The treeDepth value is : " + str(treeDepthCheck)+"\n")

#minimax must start from top of tree (0)
#the first leaf that will be reached is the leftmost (0)
mm_result = minimax(startDepth, firstLeafIndex, isMaxPlayer, scores, treeDepth, branchFactor, initialBoardState,moveIndex)

print("\n"+"The optimal value is : " + str(mm_result)+"\n")

#DEBUG:
print("EVALUATIONS at depth: "+str(treeDepth)+"\n"+ str(scores))
print("number of evaluations: "+str(len(scores)))
