import numpy as np
class Board:
    def __init__(self, holes, seeds):
        self.agentSide = 0
        self.oppSide = 1
        self.holes = holes
        self.board = np.full((2, holes+1), seeds) 
        self.board[0][holes] = 0        #North seed score pit
        self.board[1][holes] = 0        #South seed score pit

    def swapSide(self):
        if(self.agentSide == 0):
            self.agentSide = 1
            self.oppSide = 0
        else:
            self.agentSide = 0
            self.oppSide = 1

    def toString(self):
        print(self.board)

    #This is the number of holes per player (excluding scorepit)
    def getHoles(self):
        return self.holes

    def getSeeds(self, side, hole):
        return self.board[side][hole]

    def setBoard(self, state):
        self.board = state

    def setAgentSide(self, side):
        if(side == "NORTH"):
            self.agentSide = 0
            self.oppSide = 1
        else:
            self.agentSide = 1
            self.oppSide = 0

    def setBoardArray(self, board):
        newBoard = np.reshape(board, (-1, 8))
        self.board = newBoard

    def getBoard(self):
        return self.board

    def getAgentSide(self):
        return self.agentSide
    
    def getOppSide(self):
        return self.oppSide
    
    def getBoardArray(self):
        return self.board.ravel()

    def gameOver(self):
        north = self.board[0, :-1]
        south = self.board[1, :-1]
        y = np.count_nonzero(north) == 0
        z = np.count_nonzero(south) == 0
        return y or z
    
    def getOppScore(self):
        return self.board[self.oppSide][self.holes]

    def getAgentScore(self): 
        return self.board[self.agentSide][self.holes]

    def toString(self, grepWord):
        return str(grepWord) + " AGENT SIDE " + str(self.agentSide) + "\n" + str(grepWord) + " OPP SIDE " + str(self.oppSide) + "\n" + str(grepWord) + " BOARD " + str(self.board) + "\n" 
