package MKAgentRef;

import MKAgent.Board;
import MKAgent.InvalidMessageException;
import MKAgent.Kalah;
import MKAgent.Move;
import MKAgent.MsgType;
import MKAgent.Protocol;
import MKAgent.Side;
import java.io.IOException;

public class Agent {
    protected Side ourSide;
    protected Kalah kalah;
    protected int holes;

    public Agent(int holes, int seeds) {
        this.ourSide = Side.SOUTH;
        this.holes = holes;
        this.kalah = new Kalah(new Board(holes, seeds));
    }

    protected int heuristics(Board b) {
        int ourSeeds = b.getSeedsInStore(this.ourSide);
        int oppSeeds = b.getSeedsInStore(this.ourSide.opposite());

        for(int i = 1; i <= this.holes; ++i) {
            ourSeeds += b.getSeeds(this.ourSide, i);
            oppSeeds += b.getSeeds(this.ourSide.opposite(), i);
        }

        return ourSeeds - oppSeeds;
    }

    protected int bestNextMove() {
        int bestMove = 0;
        int bestMoveHeuristics = Integer.MIN_VALUE;

        for(int i = 1; i <= this.holes; ++i) {
            Move move = new Move(this.ourSide, i);
            if (this.kalah.isLegalMove(move)) {
                Board board = new Board(this.kalah.getBoard());
                Kalah.makeMove(board, move);
                int heuristics = this.heuristics(board);
                if (heuristics > bestMoveHeuristics) {
                    bestMove = i;
                    bestMoveHeuristics = heuristics;
                }
            }
        }

        return bestMove;
    }

    protected void swap() {
        this.ourSide = this.ourSide.opposite();
    }

    public void play() throws IOException, InvalidMessageException {
        boolean maySwap = false;
        String msg = Main.recvMsg();
        MsgType msgType = Protocol.getMessageType(msg);
        if (msgType != MsgType.END) {
            if (msgType != MsgType.START) {
                throw new InvalidMessageException("Expected a start message but got something else.");
            } else {
                if (Protocol.interpretStartMsg(msg)) {
                    this.ourSide = Side.SOUTH;
                    Main.sendMsg(Protocol.createMoveMsg(1));
                } else {
                    this.ourSide = Side.NORTH;
                    maySwap = true;
                }

                while(true) {
                    msg = Main.recvMsg();
                    msgType = Protocol.getMessageType(msg);
                    if (msgType == MsgType.END) {
                        return;
                    }

                    if (msgType != MsgType.STATE) {
                        throw new InvalidMessageException("Expected a state message but got something else.");
                    }

                    Protocol.MoveTurn moveTurn = Protocol.interpretStateMsg(msg, this.kalah.getBoard());
                    if (moveTurn.move == -1) {
                        this.swap();
                    }

                    if (moveTurn.again && !moveTurn.end) {
                        msg = null;
                        int nextMove = this.bestNextMove();
                        if (maySwap) {
                            Board moveBoard = new Board(this.kalah.getBoard());
                            Kalah.makeMove(moveBoard, new Move(this.ourSide, nextMove));
                            int moveHeuristics = this.heuristics(moveBoard);
                            int swapHeuristics = -this.heuristics(this.kalah.getBoard());
                            if (swapHeuristics > moveHeuristics) {
                                this.swap();
                                msg = Protocol.createSwapMsg();
                            }
                        }

                        maySwap = false;
                        if (msg == null) {
                            msg = Protocol.createMoveMsg(nextMove);
                        }

                        Main.sendMsg(msg);
                    }
                }
            }
        }
    }
}