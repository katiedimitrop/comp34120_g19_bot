import unittest
import sys
from message import *
from contextlib import contextmanager
from io import StringIO

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestMessage(unittest.TestCase):
    def testGetMsg(self):
        self.assertEquals(getMsgType("START;North"), "START")
        self.assertEquals(getMsgType("END;"), "END")

    def testMoveMsg(self):
        with captured_output() as (out, err):
            moveMsg(3)
        output = out.getvalue().strip()
        self.assertEqual(output, 'MOVE;3')

    def testSwapMsg(self):
        with captured_output() as (out, err):
            swapMsg()
        output = out.getvalue().strip()
        self.assertEqual(output, "SWAP")

    def testIsPlayerNorth(self):
        self.assertEquals(isPlayerNorth("START;North\n"), True)
        self.assertEquals(isPlayerNorth("START;South\n"), False)

    def testStateChange(self):
        expected_outpiut = [[0,0,9,9,9,9,9,2],[1,9,8,8,8,8,8,1]]
        self.assertEquals(parseStateChange("CHANGE;2;0,0,9,9,9,9,9,2,1,9,8,8,8,8,8,1;YOU", 7), expected_outpiut)

    def testGetTurn(self):
        self.assertEquals(getTurn("CHANGE;2;0,0,9,9,9,9,9,2,1,9,8,8,8,8,8,1;YOU"), "YOU")

