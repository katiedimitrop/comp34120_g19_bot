#Will return the index of a move our agent should make (range: [1,7])
#MiniMax is a backtracking based algorithm, for each possible current move it
#looks ahead (DFS) a certain number of turns (treeDepth) then backtracks and makes a
#well informed move.

#an alternative would be to create one big tree that is used to inform multiple
#consecutive moves. But a big tree like that  would require storing.

#note: nodeindex always represents the position in the current level

import math
from sys import maxsize
import numpy as np

def minimax (curDepth, nodeIndex, isMaxTurn, scores, leafDepth, branchFactor
			, currentBoard, moveIndex):
    #DEBUG:this represents the depth
	print("D"+str(curDepth)+": ")

	# base case : leafDepth (max depth) reached
	if (curDepth == leafDepth):
		#DEBUG:Leaf index and value

		#Leaves are the only node in which the board passed to them is evaluated
		#and the score returned up

		#DEBUG
		print("EVALUATING:"+str(currentBoard))
		score = evaluateBoard(currentBoard)

		#save valuation
		scores[nodeIndex] = score

		#return to parents
		return score

	if (isMaxTurn):
		#print node description 
		playerName = "SOUTH (MAX)"

		print(playerName+ " node "+ "with state:")
		print(currentBoard)
		print('\n')

		#Child scores will be sent up and stored here
		moves = [0]*branchFactor

		#Run minimax on each child (next turns)
		for moveIndex in range (0,branchFactor):
			print("If "+ playerName + " MOVES "+str(moveIndex+1))
			print(playerName + " CHILD NO."+str(moveIndex+1)+" MM")
			print("Its state will be: ")

			#Get board produced by this move from this node
			nextBoard = makeNextBoard(isMaxTurn, currentBoard, moveIndex)
			print(str(nextBoard))

			#pass board to child
			moves[moveIndex] = minimax(curDepth + 1,
			      nodeIndex * branchFactor + moveIndex ,False, scores, leafDepth
			      ,branchFactor, nextBoard,moveIndex)
			print("End MM\n")

        #Fint max value in returned scores
		bestValue = max(moves)

        #print the result
		print("D"+str(curDepth)+": "+"MAX node no."+str(nodeIndex) +
			" value: "+ str(bestValue))

		#The end: based on the value provide a move
		if (curDepth == 0): #first recursive call has finished
			print("So "+playerName + " should now MOVE "
			+str(moves.index(max(moves))+1))

		#return max child value to parent
		return bestValue

	else:

		#print node description
		playerName = "NORTH (MIN)"
		print(playerName+ " node "+ "with state:")
		print(currentBoard)
		print('\n')

		#Child scores will be sent up and stored here
		moves = [0]*branchFactor

		#Run minimax on each child (next turns)
		for moveIndex in range(0,branchFactor):
			print("If "+ playerName + " MOVES "+str(moveIndex+1))
			print(playerName + " CHILD NO."+str(moveIndex+1)+" MM")
			print("Its state will be: ")

			#Get board produced by this move from this node
			nextBoard = makeNextBoard(isMaxTurn, currentBoard, moveIndex)
			print(str(nextBoard))

			#pass board to child
			moves[moveIndex] = minimax(curDepth + 1,
			 				nodeIndex * branchFactor + moveIndex, True, scores,
							leafDepth,branchFactor, currentBoard,moveIndex)

		#find min child value
		bestValue = min(moves)

        #print the result
		print("D"+str(curDepth)+": "+"MIN node no."+str(nodeIndex) +
			" value: "+ str(bestValue))

		#The end: based on the value provide a move
		if (curDepth == 0): #first recurive call end
			print("So "+playerName + " should now MOVE "+str(moves.index(min(moves))+1))

	    #return min child value to parent
		return bestValue

def makeNextBoard(fromMaxTurn, currentBoard, moveIndex):
	curBoard = currentBoard.copy()
	if (fromMaxTurn):
		startPit = moveIndex + 8
		skipScoreOne = True #must skip first pit when sowing
		skipScoreTwo = False
	else:
		startPit = moveIndex
		skipScoreOne = False
		skipScoreTwo = True
	#collect the seeds, emptying the pit
	seedStash = curBoard[startPit]
	curBoard[startPit] = 0
	curPit = startPit
	#sow the seeds anti-clockwise
	while seedStash > 0:
		#move to next curpit
		if (curPit == 15):
			curPit = 0 #end of array was reached, reset
		else:
			curPit +=1
		if not((skipScoreOne and curPit == 7) or(skipScoreTwo and curPit == 15) ):
			curBoard[curPit]+=1
			seedStash-=1
	return curBoard

def evaluateBoard(board):
	#treat pieces on a side as equivalent to being in that side's score
	seedsOnMaxSide = sum(board[8:15])
	seedsOnMinSide = sum(board[0:7])

	score = seedsOnMaxSide - seedsOnMinSide
	#south - north
	return score



branchFactor = 7

#initialize default board state
columns = 16;
initialBoard = [0 for x in range(columns)]
for col in range (0,8):
	initialBoard[col] = 7
	initialBoard[col+8] = 7
initialBoard[7] = 0
initialBoard[15] = 0

maxTreeDepth = 1
totalNoOfLeaves = branchFactor ** maxTreeDepth

#Initialize tree leave evaluation holders
scores = [0]* totalNoOfLeaves


moveIndex = 0

#DEBUG: instead of creating heuristics in the tree Leaves
#I created random ones to test the tree
#scores = np.random.randint(-98,98, totalNoOfLeaves)


#DEBUG:
maxTreeDepthCheck = math.log(len(scores), branchFactor)
print("The maxTreeDepth value is : " + str(maxTreeDepthCheck)+"\n")


startDepth = 0
firstIndex = 0

#South is maximising player, set to 1 to run as North
isMaxPlayer = 1

#minimax must start from top of tree (0)
#First and only index at D0 is 0
mmResult = minimax(startDepth, firstIndex, isMaxPlayer, scores, maxTreeDepth
				,branchFactor, initialBoard, moveIndex)

print("\n"+"The optimal value is : " + str(mmResult)+"\n")

#DEBUG:
print("Leaf scores: "+ str(scores))
print("Number of evaluations: "+str(len(scores)))
