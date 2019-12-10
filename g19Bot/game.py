import message as msg
import manc_alphabeta as ab
import manc_minimax as mm
import sys
from Board import *
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--depth", dest = "depth", default = 14, help="Depth of Search", type=int)
parser.add_argument("-m", "--method", dest = "method", default = "AB", help="Search Method")
args = parser.parse_args()
moveNumber = 0
oppMove = 0

def makeSwap():
    global board
    board.swapSide()

def makeMove(changeM):
    global board
    global moveNumber
    
    moveNumber = moveNumber + 1
    seedNum = 0
    pitIndex = 7
    bestPit = 7

    while (pitIndex >= 1):
        seedNum = board.getSeeds(board.agentSide,pitIndex)
        # If current pit is empty, move on to next pit
        if (seedNum == 0):
          pitIndex-=1

        elif (seedNum + pitIndex == 7):
          bestPit = pitIndex

          break
        # Move that gets a seed in final pit and some in opponents pit (second best)
        elif (seedNum + pitIndex >= 7):
          bestPit = pitIndex
          pitIndex-=1

        # Any other viable move
        else:
          bestPit = pitIndex
          pitIndex-=1


    #avoid sending START message to minimax
    if 'CHANGE' in changeM:
        #uncomment to try debugging
        if(args.method == "AB"):
          bestPit = ab.run_ab(changeM, board, args.depth)
        else:
          bestPit = mm.run_mm(changeM, board.agentSide)
        #waiting here until result is available

    msg.moveMsg(bestPit)


def changeProtocol(line):
    global oppMove
    global board
    boardState = msg.parseStateChange(line, board.getHoles())
    board.setBoard(boardState)

    if(msg.isSwap(line)):
        makeSwap()
    if(msg.getTurn(line) == "YOU\n"):
        makeMove(line)
    else:
      oppMove = oppMove + 1

def startProtocol(line):
    if(msg.isPlayerNorth(line) == True):
        board.setAgentSide("NORTH")
        swap_possible = True
    else:
        board.setAgentSide("SOUTH")
        makeMove(line)

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
      try:
        line = sys.stdin.readline()
      except:
        sys.stderr.write("Something went wrong", sys.exc_info()[0])

      sys.stdin.flush()
      msgType = msg.getMsgType(line)
      if (msgType == "END"):
        break
      messageAction(line, msgType)
      time.sleep(0)
  except:
    sys.stderr.write("Something went wrong", sys.exc_info()[0])


board = Board(7,7)
swap_possible = False
run_game()