import sys

def getMsgType(line):  
    if (line == "END\n"):
        return "END"
    words = line.split(";")
    if (words[0] == "START"):
        return "START"
    elif (words[0] == "CHANGE"):
        return "END"
    else:
        return "END"

def moveMsg(holeNo):
    print("MOVE;" + str(holeNo) + "\n")

def swapMsg():
    print("SWAP\n")

def isPlayerNorth(line):
    words = line.split(";")
    if(words[1] == "NORTH\n"):
        return True
    return False
