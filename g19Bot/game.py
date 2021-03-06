import message as msg
import manc_alphabeta as ab
import sys
from Board import *
import time



def makeSwap():
    board.swapSide()

def makeMove(changeM):
    seedNum = 0
    pitIndex = 7
    bestPit = 7
    #print("GOt here")
    f.write("Searching for best move \n")
    while (pitIndex >= 1):
        seedNum = board.getSeeds(board.agentSide,pitIndex)
        # If current pit is empty, move on to next pit
        if (seedNum == 0):
          pitIndex-=1
          #f.write("PIT EMPTY \n")
          #f.write("Current pit index "+str(pitIndex)+"\n")
          #f.write("Current seed number "+str(seedNum)+"\n")
          #f.write("Current best pit "+str(bestPit)+"\n")
        # Move that makes final seed land in score pit giving extra move (best)
        elif (seedNum + pitIndex == 7):
          bestPit = pitIndex
          #f.write("BEST MOVE \n")
          #f.write("Current pit index "+str(pitIndex)+"\n")
          #f.write("Current seed number "+str(seedNum)+"\n")
          #f.write("Current best pit "+str(bestPit)+"\n")
          break
        # Move that gets a seed in final pit and some in opponents pit (second best)
        elif (seedNum + pitIndex >= 7):
          bestPit = pitIndex
          pitIndex-=1
          #f.write("SECOND BEST \n")
          #f.write("Current pit index "+str(pitIndex)+"\n")
          #f.write("Current seed number "+str(seedNum)+"\n")
          #f.write("Current best pit "+str(bestPit)+"\n")


        # Any other viable move
        else:
          bestPit = pitIndex
          pitIndex-=1
          #f.write("VIABLE MOVE \n")
          #f.write("Current pit index "+str(pitIndex)+"\n")
          #f.write("Current seed number "+str(seedNum)+"\n")
          #f.write("Current best pit "+str(bestPit)+"\n")
        #debug statements
        #f.write("Current pit index "+str(pitIndex)+"\n")
        #f.write("Current seed number "+str(seedNum)+"\n")

    #avoid sending START message to minimax
    if 'CHANGE' in changeM:
        #uncomment to try debugging
        bestPit = ab.run(changeM,f,board)
        #waiting here until result is available

    f.write("MOVE;"+str(bestPit)+"\n")

    msg.moveMsg(bestPit)


def changeProtocol(line):
    boardState = msg.parseStateChange(line, board.getHoles())
    board.setBoard(boardState)

    if(msg.isSwap(line)):
        makeSwap()
    if(msg.getTurn(line) == "YOU\n"):
        #board.toString()
        makeMove(line)

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
      f.write("READING LINE\n")
      try:
        line = sys.stdin.readline()
      except:
        f.write("Problem reading engine response\n")
      #f.write("GOT HERE\n")
      f.write(line)
      sys.stdin.flush()
      msgType = msg.getMsgType(line)
      if (msgType == "END"):
        break
      messageAction(line, msgType)
      time.sleep(0)
      #DEBUG: score pits
      #scoreNorth = board.getSeeds(0,0)
      #scoreSouth = board.getSeeds(1,0)
      #f.write("Pit no:"+str(0)+"\n")
      #f.write("North score:"+ str(scoreNorth)+"\n")
      #f.write("South score:"+str(scoreSouth)+"\n")


     #DEBUG: for each pit print out the number of seed in it
      #for pit in range(1,8):
          #seedNorth = board.getSeeds(0,pit)
          #seedSouth = board.getSeeds(1,pit)
          #f.write("Pit no:"+str(pit)+"\n")
          #f.write("North seeds:"+ str(seedNorth)+"\n")
          #f.write("South seeds:"+str(seedSouth)+"\n")
        #board.toString()      #uncomment to debug
  except:
    sys.stderr.write("Something went wrong", sys.exc_info()[0])


board = Board(7,7)
swap_possible = False
f = open('LOG.txt','w')
run_game()
f.close()
