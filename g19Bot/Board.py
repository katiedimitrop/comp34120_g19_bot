class Board:
    def __init__(self, holes, seeds):
        self.agentSide = 0
        self.holes = holes
        self.board = [[seeds] * (holes + 1) for i in range(2)]
        self.board[0][0] = 0        #North seed score pit
        self.board[1][0] = 0        #South seed score pit

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
        if(self.agentSide == 0):
            return "NORTH"
        else:
            return "SOUTH"
