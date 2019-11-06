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
        self.assertEqual(sideNorthBoard.getAgentSide(), "NORTH")

    def testSetSideSouth(self):
        sideSouthBoard = Board(2,3)
        sideSouthBoard.setAgentSide("SOUTH")
        self.assertEqual(sideSouthBoard.getAgentSide(), "SOUTH")

