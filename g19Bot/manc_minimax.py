#Will return the index of a move our agent should make (range: [1,7])
#MiniMax is a backtracking based algorithm, for each possible current move it
#looks ahead (DFS) a certain number of turns (treeDepth) then backtracks and makes a
#well informed move.

#an alternative would be to create one big tree that is used to inform multiple
#consecutive moves. But a big tree like that  would require storing.

#note: nodeindex always represents the position in the current level

import math
import sys
import numpy as np

bestMove = np.NaN
def minimax (curDepth, nodeIndex, isMaxTurn, scores, leafDepth, branchFactor
			, currentBoard, moveIndex):
	global bestMove
	moveIndex = 0
	#DEBUG:this represents the depth



	# base case : leafDepth (max depth) reached
	if (curDepth == leafDepth):
		#Leaves are the only node in which the board passed to them is evaluated
		#and the score returned up
		score = evaluateBoard(currentBoard)
		scores[nodeIndex] = score
		#return to parents
		return score

	if (isMaxTurn):
		#print node description
		playerName = "SOUTH (MAX)"

		#Child scores will be sent up and stored here
		moves = [0]*branchFactor
		noOfIllegalMoves = 0
		#Run minimax on each child (next turns)
		for moveIndex in range (0,branchFactor):

			if moveIsLegal(moveIndex,currentBoard, isMaxTurn):
				#Get board produced by this move from this node
				nextBoard = makeNextBoard(isMaxTurn, currentBoard, moveIndex)
				#by default next turn is opp's (Min's)
				maxTurn = False
				playerIsMax = True
				#however there is a move that can give an extra turn
				if givesExtraTurn(moveIndex,currentBoard, playerIsMax):
					maxTurn = True

				#pass board to child
				moves[moveIndex] = minimax(curDepth + 1,
				      nodeIndex * branchFactor + moveIndex ,maxTurn, scores, leafDepth
				      ,branchFactor, nextBoard,moveIndex)

			else:
				#don't pass board or recurse, evaluate Node here
				moves[moveIndex] = np.NaN
				noOfIllegalMoves +=1

		if noOfIllegalMoves == 7:
			leafDepth = curDepth +1
			return np.NaN
        #isolate only non nan values and find max child value
		nonNan = filter(lambda v: v==v, moves.copy())

		#if len(nonNan) > 0:
		bestValue = max(nonNan)
		#else:
			#bestValue = np.NaN


		#The end: based on the value provide a move
		if (curDepth == 0): #first recursive call has finished
			bestMove= moves.index(bestValue)+1
		#return max child value to parent
		return bestValue

	else:

		#print node description
		playerName = "NORTH (MIN)"
		#Child scores will be sent up and stored here
		moves = [0]*branchFactor
		noOfIllegalMoves = 0
		#Run minimax on each child (next turns)
		for moveIndex in range(0,branchFactor):

			if moveIsLegal(moveIndex,currentBoard,isMaxTurn):
				#Get board produced by this move from this node
				nextBoard = makeNextBoard(isMaxTurn, currentBoard, moveIndex)

				#by default next turn is opp's (Max's)
				maxTurn = True
				playerIsMax = False
				#however there is a move that can give an extra turn
				if givesExtraTurn(moveIndex,currentBoard, playerIsMax):
					maxTurn = False

				#pass board to child
				moves[moveIndex] = minimax(curDepth + 1,
				 				nodeIndex * branchFactor + moveIndex, maxTurn, scores,
								leafDepth,branchFactor, nextBoard,moveIndex)
			else:
				#don't pass board or recurse, evaluate Node here
				moves[moveIndex] = np.NaN
				noOfIllegalMoves +=1

		if noOfIllegalMoves == 7:
			leafDepth = curDepth +1
			return np.NaN

		#isolate only non nan values and find min child value
		nonNan = filter(lambda v: v==v, moves.copy())
		#for non in nonNan

		bestValue = min(nonNan)

		#The end: based on the value provide a move
		if (curDepth == 0): #first recurive call end
			bestMove = moves.index(bestValue)+1


	    #return min child value to parent
		return bestValue

def makeNextBoard(fromMaxTurn, currentBoard, moveIndex):
	resBoard = currentBoard.copy()
	NScorePit = 7
	SScorePit = 15

	if (fromMaxTurn): #move is being made by South(MAX)
		movePit = moveIndex + 8
		leftMostPit = 8
		rightMostPit = 14 #excluding score pit
		scorePit = 15
		acrossIncrement = -8
		skipScoreOne = True #must skip first pit when sowing
		skipScoreTwo = False

	else:
		movePit = moveIndex
		leftMostPit = 0
		rightMostPit = 6
		scorePit = 7
		acrossIncrement = 8
		skipScoreOne = False
		skipScoreTwo = True

	#collect the seeds, emptying the pit
	seedStash = resBoard[movePit]
	resBoard[movePit] = 0
	curPit = movePit

	#sow the seeds anti-clockwise
	while seedStash > 0:
		#find next pit index
		if (curPit == SScorePit):
			curPit = 0 #end of array was reached, reset
		else:
			curPit +=1

		#if the pit index isn't opps score pit, put a seed in
		if not((skipScoreOne and curPit == NScorePit) or
				(skipScoreTwo and curPit == SScorePit)):
			resBoard[curPit]+=1
			seedStash-=1

	#if player's last seed ended up in one of their empty playable pits
	if ((resBoard[curPit] == 1) and (leftMostPit<= curPit <= rightMostPit)):
	#take whatever is across and place it in player's score pit
		resBoard[scorePit]+=resBoard[curPit+acrossIncrement]
		#empty opp's pit
		resBoard[curPit+acrossIncrement] = 0
	return resBoard

def givesExtraTurn(moveIndex,currentBoard, fromMaxTurn):
	resBoard = currentBoard.copy()
	NScorePit = 7
	SScorePit = 15

	if (fromMaxTurn): #move is being made by South(MAX)
		movePit = moveIndex + 8
		scorePit = 15
		skipScoreOne = True #must skip first pit when sowing
		skipScoreTwo = False

	else:
		movePit = moveIndex
		scorePit = 7
		skipScoreOne = False
		skipScoreTwo = True

	#collect the seeds, emptying the pit
	seedStash = resBoard[movePit]
	resBoard[movePit] = 0
	curPit = movePit

	#sow the seeds anti-clockwise
	while seedStash > 0:
		#find next pit index
		if (curPit == SScorePit):
			curPit = 0 #end of array was reached, reset
		else:
			curPit +=1

		#if the pit index isn't opps score pit, put a seed in
		if not((skipScoreOne and curPit == NScorePit) or
				(skipScoreTwo and curPit == SScorePit)):
			resBoard[curPit]+=1
			seedStash-=1

	return curPit == scorePit

def evaluateBoard(board):
	#treat pieces on a side as equivalent to being in that side's score
	seedsOnMaxSide = sum(board[8:15])
	seedsOnMinSide = sum(board[0:7])

	score = seedsOnMaxSide - seedsOnMinSide
	#south - north
	return score

def moveIsLegal(moveIndex,board,isMaxTurn):
	if (isMaxTurn):
		moveIndex = moveIndex + 8
	return board[moveIndex] != 0 #true if move is legal


#-------------------------------Implementation----------------------------------
def run_minimax(initialBoard,isMaxPlayer):
	branchFactor = 7
	maxTreeDepth = 5
	totalNoOfLeaves = branchFactor ** maxTreeDepth
	#Initialize tree leave evaluation holders
	scores = [np.NaN]* totalNoOfLeaves
	moveIndex = 0

	#DEBUG:
	maxTreeDepthCheck = math.log(len(scores), branchFactor)
	startDepth = 0
	firstIndex = 0
	#South is maximising player, set to 1 to run as North
	origBoard = initialBoard
	#minimax must start from top of tree (0)
	#First and only index at D0 is 0
	mmResult = minimax(startDepth, firstIndex, isMaxPlayer, scores, maxTreeDepth
					,branchFactor, initialBoard, moveIndex)

	testmyboard = makeNextBoard(True, origBoard, bestMove)
	return bestMove

def run_mm(changeM,isPlayerSouth):
	words = changeM.split(";")
	state = words[2].split(",")
	state = [int(word) for word in state]
	return run_minimax(state,isPlayerSouth)

