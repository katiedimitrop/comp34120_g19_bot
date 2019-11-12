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
    pits = holes #excluding score pit
    boardArray = [[0] * (pits+1) for i in range(2)] #initialise empty 2D array
    #for all pits except score pit
    for stateIndex in range(0, pits): #0 to 7
        boardArray[0][stateIndex +1] = int(state[stateIndex])
        boardArray[1][stateIndex +1] = int(state[stateIndex + pits])

    boardArray[0][0] = int(state[pits+1])
    boardArray[1][0] = int(state[2*(pits+1)])
    return boardArray

def isSwap(line):
    words = line.split(";")
    if(words[1] == "SWAP"):
        return True
    return False

def getTurn(line):
    words = line.split(";")
    return(words[3])
