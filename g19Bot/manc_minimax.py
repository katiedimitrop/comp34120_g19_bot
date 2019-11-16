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
log = open('MM_OUT.txt','w')
def minimax (curDepth, nodeIndex, isMaxTurn, scores, leafDepth, branchFactor
			, currentBoard, moveIndex):
	global log
	global bestMove
	#DEBUG:this represents the depth
	log.write("\nD"+str(curDepth)+": ")


	# base case : leafDepth (max depth) reached
	if (curDepth == leafDepth):
		#DEBUG:Leaf index and value

		#Leaves are the only node in which the board passed to them is evaluated
		#and the score returned up

		#DEBUG
		log.write("EVALUATING:"+str(currentBoard))
		score = evaluateBoard(currentBoard)
        #DEBUG: test MM output for NaN evaluations
		#if nodeIndex == 3:
			#score = np.NaN
		#save valuation
		scores[nodeIndex] = score

		#return to parents
		return score

	if (isMaxTurn):
		#print node description
		playerName = "SOUTH (MAX)"
		log.write("-----------------"+playerName+ " node "+ "with state:")
		log.write(str(currentBoard))
		log.write("-----------------\n")

		#Child scores will be sent up and stored here
		moves = [0]*branchFactor

		#Run minimax on each child (next turns)
		for moveIndex in range (0,branchFactor):
			log.write("If "+ playerName + " MOVES "+str(moveIndex+1)+"\n")
			log.write(playerName + " CHILD NO."+str(moveIndex+1)+" MM\n")
			log.write("Its state will be: \n")

			if moveIsLegal(moveIndex,currentBoard, isMaxTurn):
				#Get board produced by this move from this node
				nextBoard = makeNextBoard(isMaxTurn, currentBoard, moveIndex)
				log.write(str(nextBoard))

				#pass board to child
				moves[moveIndex] = minimax(curDepth + 1,
				      nodeIndex * branchFactor + moveIndex ,False, scores, leafDepth
				      ,branchFactor, nextBoard,moveIndex)
				log.write("\nEnd MM\n")
			else:
				#don't pass board or recurse, evaluate Node here
				log.write("THAT'S ILLEGAL!\n")
				moves[moveIndex] = np.NaN

        #isolate only non nan values and find max child value
		nonNan = filter(lambda v: v==v, moves.copy())

		#if len(nonNan) > 0:
		bestValue = max(nonNan)
		#else:
			#bestValue = np.NaN

        #print the result
		log.write("D"+str(curDepth)+": "+"MAX node no."+str(nodeIndex) +
			" value: "+ str(bestValue)+"\n")

		#The end: based on the value provide a move
		if (curDepth == 0): #first recursive call has finished
			log.write("So "+playerName + " should now MOVE "
			+str(moves.index(bestValue)+1)+"\n")

			bestMove= moves.index(bestValue)+1
		#return max child value to parent
		return bestValue

	else:

		#print node description
		playerName = "NORTH (MIN)"
		log.write("-----------------"+playerName+ " node "+ "with state:")
		log.write(str(currentBoard))
		log.write("-----------------\n")

		#Child scores will be sent up and stored here
		moves = [0]*branchFactor

		#Run minimax on each child (next turns)
		for moveIndex in range(0,branchFactor):
			log.write("If "+ playerName + " MOVES "+str(moveIndex+1)+"\n")
			log.write(playerName + " CHILD NO."+str(moveIndex+1)+" MM\n")
			log.write("Its state will be: ")

			if moveIsLegal(moveIndex,currentBoard,isMaxTurn):
				#Get board produced by this move from this node
				nextBoard = makeNextBoard(isMaxTurn, currentBoard, moveIndex)
				log.write(str(nextBoard))

				#pass board to child
				moves[moveIndex] = minimax(curDepth + 1,
				 				nodeIndex * branchFactor + moveIndex, True, scores,
								leafDepth,branchFactor, nextBoard,moveIndex)
				log.write("\nEnd MM\n")
			else:
				#don't pass board or recurse, evaluate Node here
				log.write("THAT'S ILLEGAL!\n")
				moves[moveIndex] = np.NaN


		#isolate only non nan values and find min child value
		nonNan = filter(lambda v: v==v, moves.copy())
		#for non in nonNan

		bestValue = min(nonNan)


        #print the result
		log.write("D"+str(curDepth)+": "+"MIN node no."+str(nodeIndex) +
			" value: "+ str(bestValue)+"\n")

		#The end: based on the value provide a move
		if (curDepth == 0): #first recurive call end
			log.write("So "+playerName + " should now MOVE "
			+str(moves.index(bestValue)+1)+"\n")

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
	global log
	branchFactor = 7

	#initialize default board state
	#columns = 16;
	#initialBoard = [0 for x in range(columns)]
	#debug for testing capture (Move 1) and illegal move (4)
	#initialBoard = [7,7,7,7,7,7,7,0,3,7,7,0,7,7,7,4]
	#initialBoard = [7,7,7,7,7,7,7,0,7,7,7,7,7,7,7,0]

	maxTreeDepth = 4

	totalNoOfLeaves = branchFactor ** maxTreeDepth

	#Initialize tree leave evaluation holders
	scores = [np.NaN]* totalNoOfLeaves


	moveIndex = 0

	#DEBUG: instead of creating heuristics in the tree Leaves
	#I created random ones to test the tree
	#scores = np.random.randint(-98,98, totalNoOfLeaves)

	#DEBUG:
	maxTreeDepthCheck = math.log(len(scores), branchFactor)
	log.write("The maxTreeDepth value is : " + str(maxTreeDepthCheck)+"\n")


	startDepth = 0
	firstIndex = 0

	#South is maximising player, set to 1 to run as North


	#minimax must start from top of tree (0)
	#First and only index at D0 is 0
	mmResult = minimax(startDepth, firstIndex, isMaxPlayer, scores, maxTreeDepth
					,branchFactor, initialBoard, moveIndex)


	log.write("\n"+"The optimal value is : " + str(mmResult)+"\n")
	log.write("\n"+"The best move is : " + str(bestMove)+"\n")

	#DEBUG:
	log.write("Leaf scores: "+ str(scores)+"\n")
	log.write("Number of evaluations: "+str(len(scores))+"\n")
	return bestMove

def run(changeM,f,isPlayerSouth):
	#parse the engine changeMsg in order to produce array
	words = changeM.split(";")
	state = words[2].split(",")

	#f.write("\nHello from minimax!\n")
	#f.write("BOARD:"+str(state)+"\n")
	#f.write(str(isPlayerSouth)+"\n")
	state = [int(word) for word in state]

	#Debug:
	#f.write("Minimax: MOVE "+str(move))
	f.write("Best Move:"+str(run_minimax(state,isPlayerSouth)) + "\n")
	return run_minimax(state,isPlayerSouth)


#run_minimax()
