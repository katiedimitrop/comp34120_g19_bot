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

MAXDEPTH = 5
log = open('MM_OUT.txt','w')
def alphabeta (curDepth, isMaxTurn, branchFactor, currentBoard, alpha, beta):
	global log
	global MAXDEPTH
	
	value = 0
	log.write("\nD"+str(curDepth)+": ")

	# base case : leafDepth (max depth) reached or Game Over 
	if (curDepth == MAXDEPTH) or (currentBoard.gameOver()):
		log.write("EVALUATING:"+str(currentBoard.getBoardArray()) + "\n")
		value = evaluateBoard(currentBoard)

	#If player turn: set find max value and set alpha
	elif (isMaxTurn):
		value = -9999
		prune = False
		playerName = "(OUR PLAYER) MAX"
		log.write("-----------------"+playerName+ " node "+ "with state:")
		log.write(str(currentBoard.getBoardArray()))
		log.write("-----------------\n")

		#Child scores will be sent up and stored here
		#Run alphabeta on each child (next turns)
		for moveIndex in range (0,branchFactor):
			if not prune:
				log.write("If "+ playerName + " MOVES "+str(moveIndex + 1)+"\n")
				log.write(playerName + " CHILD NO."+str(moveIndex + 1)+" MM\n")
				log.write("Its state will be: \n")

				if moveIsLegal(moveIndex,currentBoard, isMaxTurn):
					#Get board produced by this move from this node
					nextBoard = makeNextBoard(currentBoard.getAgentSide(), copy.deepcopy(currentBoard), moveIndex)
					log.write(str(nextBoard.getBoardArray()) + "\n")
					#by default next turn is opp's (Min's)
					maxTurn = False
					playerIsMax = True
					#however there is a move that can give an extra turn
					if givesExtraTurn(moveIndex,currentBoard, playerIsMax):
						maxTurn = True

					#pass board to child
					value = max(value, alphabeta(curDepth + 1, maxTurn, branchFactor, nextBoard, alpha, beta))
					alpha = max(value, alpha)
					if alpha >= beta:
						log.write("PRUNE\n")
						prune = True
				else:
					#if not legal, set alpha really high so it isnt used and do not recurse
					alpha = -9999

	#if not player turn: find minimum value and set beta 
	else:
		prune = False
		value = 9999
		#print node description
		playerName = "(OPPONENT) MIN"
		log.write("-----------------"+playerName+ " node "+ "with state:")
		log.write(str(currentBoard.getBoardArray()))
		log.write("-----------------\n")

		for moveIndex in range (0,branchFactor):
			if not prune:
				log.write("If "+ playerName + " MOVES "+str(moveIndex + 1)+"\n")
				log.write(playerName + " CHILD NO."+str(moveIndex +1)+" MM\n")
				log.write("Its state will be: ")

				if moveIsLegal(moveIndex,currentBoard,isMaxTurn):
					#Get board produced by this move from this node
					nextBoard = makeNextBoard(currentBoard.getOppSide(), copy.deepcopy(currentBoard), moveIndex)
					log.write(str(nextBoard.getBoardArray()) + "\n")

					#by default next turn is opp's (Max's)
					maxTurn = True
					playerIsMax = False
					#however there is a move that can give an extra turn
					if givesExtraTurn(moveIndex,currentBoard, playerIsMax):
						maxTurn = False

					#pass board to child
					value = min(value, alphabeta(curDepth + 1, maxTurn, branchFactor, nextBoard, alpha, beta))
					beta = min(value, beta)
					if alpha >= beta:
						prune = True
						log.write("PRUNE\n")
					return value
				else:
					# Move Illegal, set Beta to extremely high value
					beta = 9999
	return value
	

def makeNextBoard(side, currentBoard, moveIndex):
	resBoard = currentBoard.getBoardArray()
	NScorePit = 7
	SScorePit = 15

	if (side == 1): #move is being made by South(MAX)
		movePit = moveIndex + 7
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
	board = np.reshape(resBoard, (-1, 8))
	currentBoard.setBoard(board)
	return currentBoard

def givesExtraTurn(moveIndex,currentBoard, fromMaxTurn):
	global log
	resBoard = currentBoard.getBoardArray()
	NScorePit = 7
	SScorePit = 15
	if(fromMaxTurn):	
		index = currentBoard.agentSide
	else: 
		index = currentBoard.getOppSide()
	
	if (index == 1): #move is being made by South(MAX)
		movePit = moveIndex + 7
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

# evaluateBoard : works out the value of the board based on hueristic
def evaluateBoard(board):
	resBoard = board.getBoardArray()
	seedsOnSouthSide = sum(resBoard[8:15])
	seedsOnNorthSide = sum(resBoard[0:7])
	if (board.agentSide == 1):
		return seedsOnSouthSide - seedsOnNorthSide
	return seedsOnNorthSide - seedsOnSouthSide

# moveIsLegal : True if legal, False if Illegal
def moveIsLegal(moveIndex,board,isMaxTurn):
	if (isMaxTurn):
		return board.getSeeds(board.agentSide, moveIndex) != 0
	return board.getSeeds(board.getOppSide(), moveIndex) != 0 


#-------------------------------Implementation----------------------------------
def run_alphabeta(initialBoard):
	global log
	branchFactor = 7
	value = alpha = -9999
	beta = 9999
	moveIndex = move = 0
	prune = False

	#check available moves and their value
	for moveIndex in range (0,branchFactor):
		if moveIsLegal(moveIndex, initialBoard, True):
			#Get board produced by this move from this node
			nextBoard = makeNextBoard(initialBoard.getAgentSide(), copy.deepcopy(initialBoard), moveIndex)
			#by default next turn is opp's (Min's)
			maxTurn = False
			playerIsMax = True
			#check for extra turn
			if givesExtraTurn(moveIndex, nextBoard, playerIsMax):
				maxTurn = True
			log.write(str(nextBoard.getBoardArray()) + "\n")
			value = max(value, alphabeta(0, True, branchFactor, nextBoard, alpha, beta))
			if alpha < value: 
				alpha = value
				bestMove = moveIndex

	log.write("\n"+"The optimal value is : " + str(value)+"\n")
	log.write("\n"+"The best move is : " + str(bestMove+1)+"\n")

	return bestMove + 1

def run(changeM,f,board):
	#parse the engine changeMsg in order to produce array
	words = changeM.split(";")
	state = words[2].split(",")
	state = [int(word) for word in state]
	statearray = np.reshape(state, (-1, 8))
	board.setBoard(statearray)
	return run_alphabeta(board)
#run_minimax()
