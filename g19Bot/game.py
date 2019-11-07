import message as msg
import sys
from Board import *

def makeSwap():
    board.swapSide()

def makeMove():
    seedNum = 0
    pitIndex = 0
    f.write("Searching for best move \n")
    #Strategy: find next pit where pitNum > 0
    while (seedNum == 0):
        seedNum = board.getSeeds(board.agentSide,pitIndex)
        #debug statements
        #f.write("Current pit index "+str(pitIndex)+"\n")
        #f.write("Current seed number "+str(seedNum)+"\n")
        pitIndex+=1
    f.write("MOVE;"+str(pitIndex)+"\n")
    msg.moveMsg(pitIndex)


def changeProtocol(line):
    boardState = msg.parseStateChange(line, board.getHoles())
    board.setBoard(boardState)
    #board.toString()
    if(msg.isSwap(line)):
        makeSwap()
    if(msg.getTurn(line) == "YOU\n"):
        makeMove()

def startProtocol(line):
    if(msg.isPlayerNorth(line) == True):
        board.setAgentSide("NORTH")
        swap_possible = True
    else:
        board.setAgentSide("SOUTH")
        makeMove()

def messageAction(line, msgType):
    #print("messageAction")
    if(msgType == "START"):
        startProtocol(line)
    if(msgType == "CHANGE"):
        changeProtocol(line)



def run_game():
  try:
    #board.toString()        #uncomment to debug
    while True:
      f.write("READING LINE\n")
      try:
        line = sys.stdin.readline()
      except:
        f.write("FUCK THIS\n")
      f.write("GOT HERE\n")
      f.write(line)
      sys.stdin.flush()
      msgType = msg.getMsgType(line)
      if (msgType == "END"):
        break
      messageAction(line, msgType)
        #board.toString()      #uncomment to debug
  except:
    sys.stderr.write("Something went wrong", sys.exc_info()[0])


board = Board(7,7)
swap_possible = False
f = open('LOG.txt','w')
run_game()
f.close()
