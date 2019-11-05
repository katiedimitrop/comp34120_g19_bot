import message as msg
import sys
from Board import * 


def makeMove():
    msg.moveMsg(1)

def startProtocol(line):
    if(msg.isPlayerNorth(line) == True):
        board.setAgentSide("NORTH")
        swap_possible = True
    else:
        board.setAgentSide("SOUTH")
        makeMove()

def messageAction(line, msgType):
    if(msgType == "START"):
        startProtocol(line)

def run_game():
  try:
    #board.toString()        #uncomment to debug
    while True:
      line = sys.stdin.readline()
      msgType = msg.getMsgType(line)
      if (msgType == "END"):
          break
      messageAction(line, msgType)
  except:
    sys.stderr.write("Something went wrong", sys.exc_info()[0])

board = Board(7,7)
swap_possible = False  
run_game()