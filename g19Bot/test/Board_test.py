import unittest
from Board import *

class TestBoard(unittest.TestCase):
    def testInitialise(self):
        initTestBoard = Board(2, 2)
        outputArray = [[0, 2, 2], [0, 2, 2]]
        self.assertListEqual(initTestBoard.getBoard(), outputArray)

    def testSetSideNorth(self):
        sideNorthBoard = Board(2,3)
        sideNorthBoard.setAgentSide("NORTH")
        self.assertEqual(sideNorthBoard.getAgentSide(), 0)

    def testSetSideSouth(self):
        sideSouthBoard = Board(2,3)
        sideSouthBoard.setAgentSide("SOUTH")
        self.assertEqual(sideSouthBoard.getAgentSide(), 1)

    def testSetState(self):
        testStateBoard = Board(7, 7)
        inputState = [[0, 0, 9, 9, 9, 9, 9, 2], [1, 9, 8, 8, 8, 8, 8, 1]]
        testStateBoard.setBoard(inputState)
        self.assertTrue(testStateBoard.getBoard, inputState)   

