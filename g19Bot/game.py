import message as msg
import sys
from Board import * 

def makeSwap():
    board.swapSide()

def makeMove():
    f.write("MOVE;3\n")
    msg.moveMsg(3)

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
f = open('ERROR.txt','w')
run_game()