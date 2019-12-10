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
import copy

MAXDEPTH = 8
SCORE_W = 0.3
SEEDS_W = 0.2
OURCAPT_W = 0.2
OPPCAPT_W = 0.2
EXTRA_W = 0.1
def alphabeta (curDepth, isMaximizingPlayer, branchFactor, previousBoard, currentBoard, rootBoard, alpha, beta, extraTurns):
	global MAXDEPTH
	value = 0

	if (curDepth == MAXDEPTH-2) or (currentBoard.gameOver()):
		value = evaluateBoard(previousBoard,currentBoard,rootBoard, extraTurns)
		return value

	#If player turn: set find max value and set alpha
	elif (isMaximizingPlayer):
		value = -9999
		prune = False

		#Child scores will be sent up and stored here
		#Run alphabeta on each child (next turns)
		for moveIndex in range (0,branchFactor):
			if not prune:

				if moveIsLegal(moveIndex,currentBoard, isMaximizingPlayer):
					#Get board produced by this move from this node

					nextBoard = copy.deepcopy(currentBoard)
					nextArray = makeNextBoard(nextBoard.agentSide, nextBoard.getBoardArray(), moveIndex)
					nextBoard.setBoardArray(nextArray)

					#by default next turn is opp's (Min's)
					nextPlayerIsMax = False
					#unless it's a move that gives an extra turn to Max
					if givesExtraTurn(moveIndex,copy.deepcopy(currentBoard), isMaximizingPlayer):
						nextPlayerIsMax = True
						extraTurns = extraTurns + 1

					#pass board to child
					value = max(value, alphabeta(curDepth + 1, nextPlayerIsMax, branchFactor,copy.deepcopy(currentBoard), nextBoard, rootBoard, alpha, beta, extraTurns))
					alpha = max(value, alpha)
					if alpha >= beta:
						prune = True
						break
					return value
				else:
					alpha = -9999

	#if not player turn: find minimum value and set beta
	else:
		prune = False
		value = 9999
		#print node description

		for moveIndex in range (0,branchFactor):
			if not prune:
				if moveIsLegal(moveIndex,currentBoard,isMaximizingPlayer):
					#Get board produced by this move from this node

					nextBoard = copy.deepcopy(currentBoard)
					nextArray = makeNextBoard(nextBoard.oppSide, nextBoard.getBoardArray(), moveIndex)
					nextBoard.setBoardArray(nextArray)

					#by default next turn is agents (Max's)
					nextPlayerIsMax = True
					#unless it's a move that gives an extra turn to Max
					if givesExtraTurn(moveIndex,copy.deepcopy(currentBoard), isMaximizingPlayer):
						nextPlayerIsMax = False

					#pass board to child
					value = min(value, alphabeta(curDepth + 1, nextPlayerIsMax, branchFactor,copy.deepcopy(currentBoard), nextBoard,rootBoard, alpha, beta, extraTurns))	
					beta = min(value, beta)
					if alpha >= beta:
						prune = True
						break
					return value
				else:
					# Move Illegal, set Beta to extremely high value
					beta = 9999
	return value


def makeNextBoard(playerSide, currentBoard, moveIndex):
	resBoard = currentBoard
	NScorePit = 7
	SScorePit = 15

	if (playerSide == 1): #move is being made by South
		movePit = moveIndex + 8
		leftMostPit = 8
		rightMostPit = 14 #excluding score pit
		scorePit = 15
		acrossIncrement = -8
		skipSouth = False
		skipNorth = True

	else:	#move is being made by North
		movePit = moveIndex
		leftMostPit = 0
		rightMostPit = 6
		scorePit = 7
		acrossIncrement = 8
		skipSouth = True #must skip first pit when sowing
		skipNorth = False

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
		if not((skipNorth and curPit == NScorePit) or
				(skipSouth and curPit == SScorePit)):
			resBoard[curPit]+=1
			seedStash-=1


	#if player's last seed ended up in one of their empty playable pits
	if ((resBoard[curPit] == 1) and (leftMostPit<= curPit <= rightMostPit)):
	#take whatever is across and place it in player's score pit
		resBoard[scorePit]+=resBoard[curPit+acrossIncrement]
		#the scorepit across was non empty (i.e a capture occured)
		if resBoard[curPit+acrossIncrement]!=0:
			#also capture the capturing seed
			resBoard[curPit]-=1
			resBoard[scorePit]+=1
		#empty opp's pit
		resBoard[curPit+acrossIncrement] = 0

	return resBoard

def givesExtraTurn(moveIndex, currentBoard, fromMaxNode):
	resBoard = currentBoard.getBoardArray()
	NScorePit = 7
	SScorePit = 15
	if(fromMaxNode):
		index = currentBoard.agentSide
	else:
		index = currentBoard.getOppSide()

	if (index == 1): #move is being made by South
		movePit = moveIndex + 8
		scorePit = 15
		skipNorthPit = True #must skip first pit when sowing
		skipSouthPit = False

	else: #indexing for North Side
		movePit = moveIndex
		scorePit = 7
		skipNorthPit = False
		skipSouthPit = True

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
		if not((skipNorthPit and curPit == NScorePit) or
				(skipSouthPit and curPit == SScorePit)):
			resBoard[curPit]+=1
			seedStash-=1

	return curPit == scorePit

# evaluateBoard : works out the value of the board based on hueristic
def evaluateBoard(previousBoard,board,rootBoard, extraTurns):
	#global #log
	resBoard = board.getBoardArray()
	resPrevBoard = previousBoard.getBoardArray()
	resRootBoard = rootBoard.getBoardArray()

	seedsOnSouthSide = sum(resBoard[8:15])
	seedsOnNorthSide = sum(resBoard[0:7])
	scoreNorth = resBoard[7]
	scoreSouth = resBoard[15]
	prevScoreNorth = resPrevBoard[7]
	diffScoreNorth = scoreNorth - prevScoreNorth
	prevScoreSouth = resPrevBoard[15]
	diffScoreSouth = scoreSouth - prevScoreSouth

	resBoard = board.getBoardArray()
	northScorePit= 7
	southScorePit = 15



	#get all indexes where we may attack is possible
	southAttackIndexes = []
	northAttackIndexes = []
	for pitIndex in range(0,7):# [8,14] or [0,6]

		if resBoard[pitIndex] == 0 and resBoard[pitIndex+8] != 0:
			northAttackIndexes.append(pitIndex)

		if resBoard[pitIndex+8] == 0 and resBoard[pitIndex] != 0:
			southAttackIndexes.append(pitIndex+8)

	#given all those attack points find move Pit indexes where an oppotunity to
	#attack exists
	northCaptures=0
	southCaptures=0
	for attackIndex in northAttackIndexes:
		#for each move pit except it
		for moveIndex in range(0,northScorePit+1):
			if moveIndex == attackIndex:
				break
			if moveIndex < attackIndex:
				northCaptures += (resBoard[moveIndex] == attackIndex - moveIndex)
			if moveIndex > attackIndex:
				northCaptures += (resBoard[moveIndex] == (15+attackIndex) - moveIndex)

	for attackIndex in southAttackIndexes:
		#for each move pit except it
		for moveIndex in range(8,southScorePit+1):
			if moveIndex == attackIndex:
				break
			if moveIndex > attackIndex:
				southCaptures += (resBoard[moveIndex] == attackIndex - moveIndex)
			if moveIndex < attackIndex:
				southCaptures += (resBoard[moveIndex] == (15+attackIndex) - moveIndex)

	if (board.agentSide == 0): #North
		ourCaptures = northCaptures
		oppCaptures = southCaptures
	else: #South
		ourCaptures = southCaptures
		oppCaptures = northCaptures


	if (board.agentSide == 1):
		return (SCORE_W*(scoreSouth - scoreNorth)) + (SEEDS_W*(seedsOnSouthSide - seedsOnNorthSide)) + (OURCAPT_W*ourCaptures)-(OPPCAPT_W*oppCaptures) + (EXTRA_W*extraTurns)
	return (SCORE_W*(scoreNorth - scoreSouth)) + (SEEDS_W*(seedsOnNorthSide - seedsOnSouthSide)) + (OURCAPT_W*ourCaptures)-(OPPCAPT_W*oppCaptures) + (EXTRA_W*extraTurns)

# moveIsLegal : True if legal, False if Illegal
def moveIsLegal(moveIndex,board,isMaxTurn):
	if (isMaxTurn):
		return board.getSeeds(board.agentSide, moveIndex) != 0
	return board.getSeeds(board.getOppSide(), moveIndex) != 0


#-------------------------------Implementation----------------------------------
def run_alphabeta(initialBoard):
	branchFactor = 7
	value = alpha = maxValue = -9999
	beta = 9999
	moveIndex = move = 0

	for moveIndex in range (0,branchFactor):
		if moveIsLegal(moveIndex, initialBoard, True):

			nextBoard = copy.deepcopy(initialBoard)
			nextArray = makeNextBoard(nextBoard.agentSide, nextBoard.getBoardArray(), moveIndex)
			nextBoard.setBoardArray(nextArray)


			nextPlayerIsMax = False
			extraTurns = 0
			if givesExtraTurn(moveIndex, copy.deepcopy(initialBoard), True):
				nextPlayerIsMax = True
				extraTurns=extraTurns+1

			value = max(value, alphabeta(0, nextPlayerIsMax, branchFactor,copy.deepcopy(initialBoard), copy.deepcopy(nextBoard),copy.deepcopy(initialBoard), alpha, beta, extraTurns))
			if maxValue < value:
				maxValue = value
				bestMove = moveIndex
				bestBoard = nextBoard

	return bestMove + 1

def run_ab(changeM, board, depth):
	global MAXDEPTH
	MAXDEPTH = depth
	words = changeM.split(";")
	state = words[2].split(",")
	state = [int(word) for word in state]
	statearray = np.reshape(state, (-1, 8))
	board.setBoard(statearray)
	return run_alphabeta(board)
