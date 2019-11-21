import numpy as np
class Board:
    def __init__(self, holes, seeds):
        self.agentSide = 0
        self.holes = holes
        self.board = np.full((2, holes+1), seeds) 
        self.board[0][holes] = 0        #North seed score pit
        self.board[1][holes] = 0        #South seed score pit

    def swapSide(self):
        if(self.agentSide == 0):
            self.agentSide = 1
        else:
            self.agentSide = 0

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
        else:
            self.agentSide = 1

    def getBoard(self):
        return self.board

    def getAgentSide(self):
        return self.agentSide
    
    def getOppSide(self):
        if(self.agentSide == 0):
            return 1
        else:
            return 0
    
    def getBoardArray(self):
        return self.board.ravel()

    def gameOver(self):
        x = self.board[0, :-1]
        y = np.count_nonzero(x) == 0
        return y
