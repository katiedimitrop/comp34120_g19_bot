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
log = open('MANCALA_OUT.txt','w')
def alphabeta (curDepth, isMaximizingPlayer, branchFactor,previousBoard, currentBoard,rootBoard, alpha, beta, extraTurns):
	#global #log
	global MAXDEPTH

	value = 0
	log.write("\nD"+str(curDepth)+": ")

	# base case : leafDepth (max depth) reached or Game Over

	if (curDepth == MAXDEPTH-2) or (currentBoard.gameOver()):
		#log.write("EVALUATING:"+str(currentBoard.getBoardArray()) + "\n")
		value = evaluateBoard(previousBoard,currentBoard,rootBoard)
		#log.write("SKA : VALUE " + str(value) + "\n")
		#log.write("SKA : BOARD " + str(currentBoard.getBoardArray()) + "\n\n")
		log.write("EXTRATURNS " + str(extraTurns) + "\n")
		return value

	#If player turn: set find max value and set alpha
	elif (isMaximizingPlayer):
		value = -9999
		prune = False
		playerName = "(OUR PLAYER) MAX"
		#log.write("-----------------"+playerName+ " node "+ "with state:")
		#log.write(str(currentBoard.getBoardArray()))
		#log.write("-----------------\n")

		#Child scores will be sent up and stored here
		#Run alphabeta on each child (next turns)
		for moveIndex in range (0,branchFactor):
			if not prune:
				#log.write("If "+ playerName + " MOVES "+str(moveIndex + 1)+"\n")
				#log.write(playerName + " CHILD NO."+str(moveIndex + 1)+" MM\n")
				#log.write("Its state will be: \n")

				if moveIsLegal(moveIndex,currentBoard, isMaximizingPlayer):
					#Get board produced by this move from this node
					#log.write("CHAOS ====================================== \n")
					#log.write("CHAOS - BEFORE " + str(currentBoard.getBoardArray()) + "\n")
					nextBoard = copy.deepcopy(currentBoard)
					nextArray = makeNextBoard(nextBoard.agentSide, nextBoard.getBoardArray(), moveIndex)
					nextBoard.setBoardArray(nextArray)
					#log.write("CHAOS - EXITED" + str(nextBoard.getBoardArray()) + "\n")
					#log.write("CHAOS ====================================== \n")

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
						#log.write("PRUNE\n")
						prune = True
						break
					return value
				else:
					#log.write("ILLEGAL\n")
					alpha = -9999

	#if not player turn: find minimum value and set beta
	else:
		prune = False
		value = 9999
		#print node description
		playerName = "(OPPONENT) MIN"
		#log.write("-----------------"+playerName+ " node "+ "with state:")
		#log.write(str(currentBoard.getBoardArray()))
		#log.write("-----------------\n")

		for moveIndex in range (0,branchFactor):
			if not prune:
				#log.write("If "+ playerName + " MOVES "+str(moveIndex + 1)+"\n")
				#log.write(playerName + " CHILD NO."+str(moveIndex +1)+" MM\n")
				#log.write("Its state will be: ")
				if moveIsLegal(moveIndex,currentBoard,isMaximizingPlayer):
					#Get board produced by this move from this node
					#log.write("CHAOS ====================================== \n")
					#log.write("CHAOS - BEFORE " + str(currentBoard.getBoardArray()) + "\n")
					nextBoard = copy.deepcopy(currentBoard)
					nextArray = makeNextBoard(nextBoard.oppSide, nextBoard.getBoardArray(), moveIndex)
					nextBoard.setBoardArray(nextArray)
					#log.write("CHAOS - EXITED" + str(nextBoard.getBoardArray()) + "\n")
					#log.write("CHAOS ====================================== \n")

					#by default next turn is agents (Max's)
					nextPlayerIsMax = True
					#unless it's a move that gives an extra turn to Max
					if givesExtraTurn(moveIndex,copy.deepcopy(currentBoard), isMaximizingPlayer):
						nextPlayerIsMax = False
						extraTurns = extraTurns + 1

					#pass board to child
					value = min(value, alphabeta(curDepth + 1, nextPlayerIsMax, branchFactor,copy.deepcopy(currentBoard), nextBoard,rootBoard, alpha, beta, extraTurns))
					#log.write("BETA: " + str(value) + " MOVE INDEX " + str(moveIndex) + " DEPTH " +  str(curDepth) + " BOARD " + str(nextBoard.getBoardArray()) +"\n")
					beta = min(value, beta)
					if alpha >= beta:
						prune = True
						#log.write("PRUNE\n")
						break
					return value
				else:
					# Move Illegal, set Beta to extremely high value
					#log.write("ILLEGAL\n")
					beta = 9999
	return value


def makeNextBoard(playerSide, currentBoard, moveIndex):
	resBoard = currentBoard
	#log.write("\n -----------------------------------------------------\n")
	#log.write("CHAOS - MOVE " + str(moveIndex) + "\n")
	#log.write("CHAOS - SIDE " + str(playerSide) + "\n")
	#log.write("CHAOS - NOT MOVED " + str(resBoard) + "\n")
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
		#log.write("CHAOS - " + str(resBoard) + "\n")

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

	#log.write("CHAOS - MOVED " + str(resBoard) + "\n")
	#log.write("-----------------------------------------------------\n")
	return resBoard

def givesExtraTurn(moveIndex, currentBoard, fromMaxNode):
	#global #log
	#log.write("EXTRA - BEFORE " + str(currentBoard.toString("EXTRA")) + "\n")
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

	#log.write("EXTRA - AFTER " + str(currentBoard.toString("EXTRA")) + "\n")
	return curPit == scorePit

# evaluateBoard : works out the value of the board based on hueristic
def evaluateBoard(previousBoard,board,rootBoard):
	#global #log
	resBoard = board.getBoardArray()
	resPrevBoard = previousBoard.getBoardArray()
	resRootBoard = rootBoard.getBoardArray()
	log.write("phe: CURBOARD " + str(resBoard) + "\n")
	log.write("phe: PREVBOARD " + str(resPrevBoard) + "\n")
	log.write("phe: ROOTBOARD " + str(resRootBoard) + "\n")
	#log.write("SKA: BOARD " + str(resBoard) + "\n")
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
		return (scoreSouth - scoreNorth) + 0.5*(seedsOnSouthSide - seedsOnNorthSide)
	return (scoreNorth - scoreSouth) + 0.5*(seedsOnNorthSide - seedsOnSouthSide)

# moveIsLegal : True if legal, False if Illegal
def moveIsLegal(moveIndex,board,isMaxTurn):
	#log.write("LEGAL CHECKING MOVE " + str(moveIndex) + " FOR MAX NODE " + str(isMaxTurn) + "\n")
	#log.write("LEGAL CHECKING BOARD " + str(board.getBoardArray())

	if (isMaxTurn):
		#log.write("LEGAL INDEX GOT " + str(board.getSeeds(board.agentSide, moveIndex)) + "\n")
		return board.getSeeds(board.agentSide, moveIndex) != 0
	#log.write("LEGAL INDEX GOT " + str(board.getSeeds(board.getOppSide(), moveIndex)) + "\n")
	return board.getSeeds(board.getOppSide(), moveIndex) != 0


#-------------------------------Implementation----------------------------------
def run_alphabeta(initialBoard):
	#global #log
	branchFactor = 7
	value = alpha = maxValue = -9999
	beta = 9999
	moveIndex = move = 0
	#prune = False

	#log.write("\n"+"STARTING ALPHABETA WITH MAX DEPTH: " + str(MAXDEPTH)+"\n")
	#check available moves and their value
	for moveIndex in range (0,branchFactor):
		if moveIsLegal(moveIndex, initialBoard, True):
			#Get board produced by this move from this node
			#log.write("\n CHAOS MASTER ====================================== \n")
			#log.write("CHAOS ====================================== \n")
			#log.write("CHAOS - BEFORE " + str(initialBoard.getBoardArray()) + "\n")
			#log.write("ORDER:  MOVE " + str(moveIndex) + "\n")
			#log.write("ORDER: INIT BOARD \n")
			#log.write(initialBoard.toString("ORDER"))
			nextBoard = copy.deepcopy(initialBoard)
			#log.write("ORDER: COPY BOARD \n")
			#log.write(nextBoard.toString("ORDER"))
			nextArray = makeNextBoard(nextBoard.agentSide, nextBoard.getBoardArray(), moveIndex)
			nextBoard.setBoardArray(nextArray)
			#log.write("ORDER: MAKE NEXT BOARD \n")
			#log.write(nextBoard.toString("ORDER"))
			#log.write("CHAOS - EXITED" + str(nextBoard.getBoardArray()) + "\n")
			#log.write("CHAOS ====================================== \n")
			#by default next turn is opp's (Min's)

			nextPlayerIsMax = False
			extraTurns = 0
			#check for extra turn
			if givesExtraTurn(moveIndex, copy.deepcopy(initialBoard), True):
				nextPlayerIsMax = True
				extraTurns=extraTurns+1

			#log.write(str(nextBoard.getBoardArray()) + "\n")
			value = max(value, alphabeta(0, nextPlayerIsMax, branchFactor,copy.deepcopy(initialBoard), copy.deepcopy(nextBoard),copy.deepcopy(initialBoard), alpha, beta, extraTurns))
			#log.write("GRIMES MOVE : " + str(moveIndex) + " VALUE : " + str(value) + "\n")
			#log.write("GRIMES BOARD : " + str(nextBoard.getBoardArray()) + "\n")
			if maxValue < value:
				maxValue = value
				bestMove = moveIndex
				bestBoard = nextBoard

	#log.write("======== INITIAL BOARD =========\n")
	#log.write(str(initialBoard.getBoardArray()) + "\n")
	#log.write("\n"+"The optimal value is : " + str(value)+"\n")
	#log.write("\n"+"The best move is : " + str(bestMove+1)+"\n")
	#log.write("\nThe best board is " + str(bestBoard.getBoardArray()) +"\n" )

	return bestMove + 1

def run_ab(changeM,f,board, depth):
	global MAXDEPTH
	MAXDEPTH = depth
	#log.write("MAXDEPTH " + str(MAXDEPTH) + "\n")
	#parse the engine changeMsg in order to produce array
	words = changeM.split(";")
	state = words[2].split(",")
	state = [int(word) for word in state]
	statearray = np.reshape(state, (-1, 8))
	board.setBoard(statearray)
	return run_alphabeta(board)
#run_minimax()
