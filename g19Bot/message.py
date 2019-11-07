import sys

def getMsgType(line):  
    if (line == "END\n"):
        return "END"
    words = line.split(";")
    if (words[0] == "START"):
        return "START"
    elif (words[0] == "CHANGE"):
        return "CHANGE"
    else:
        return "END"

def moveMsg(holeNo):
    print("MOVE;" + str(holeNo))

def swapMsg():
    print("SWAP\n")

def isPlayerNorth(line):
    words = line.split(";")
    if(words[1] == "North\n"):
        return True
    return False

def parseStateChange(line, holes):
    words = line.split(";")
    state = words[2].split(",")
    pits = holes + 1 
    boardArray = [[0] * (pits) for i in range(2)] #initialise empty 2D array
    for i in range(0, (pits)):
        boardArray[0][i] = int(state[i])
        boardArray[1][i] = int(state[i + pits])
    return boardArray

def isSwap(line):
    words = line.split(";")
    if(words[1] == "SWAP"):
        return True 
    return False

def getTurn(line):
    words = line.split(";")
    return(words[3])




