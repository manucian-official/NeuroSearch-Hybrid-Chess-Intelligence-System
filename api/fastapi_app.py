# fastapi_app.py
# FastAPI backend for chess engine

from fastapi import FastAPI
from pydantic import BaseModel
import chess

from bitboard import Bitboard, WHITE, BLACK
from minimax import MinimaxEngine
from hybrid import HybridSearch
from mcts import MCTS

# ===============================
# INIT
# ===============================

app = FastAPI(title="Chess AI Engine API")

minimax_engine = MinimaxEngine()
hybrid_engine = HybridSearch(use_nn=True)
mcts_engine = MCTS(simulations=100)


# ===============================
# REQUEST MODELS
# ===============================

class AnalyzeRequest(BaseModel):
    fen: str
    engine: str = "hybrid"  # minimax / hybrid / mcts
    depth: int = 3


# ===============================
# UTILS
# ===============================

def fen_to_bitboard(fen: str):
    """
    Convert python-chess board -> Bitboard
    """
    board = chess.Board(fen)
    bb = Bitboard()

    piece_map = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5
    }

    for square, piece in board.piece_map().items():
        color = WHITE if piece.color == chess.WHITE else BLACK
        piece_type = piece_map[piece.piece_type]

        bb.set_piece(color, piece_type, square)

    side = WHITE if board.turn == chess.WHITE else BLACK

    return bb, side


def move_to_uci(move):
    """
    Convert Move object -> UCI string
    """
    files = "abcdefgh"
    ranks = "12345678"

    from_sq = move.from_sq
    to_sq = move.to_sq

    def sq_to_str(sq):
        return files[sq % 8] + ranks[sq // 8]

    return sq_to_str(from_sq) + sq_to_str(to_sq)


# ===============================
# ROUTES
# ===============================

@app.get("/")
def root():
    return {"message": "Chess AI Engine is running 🚀"}


@app.post("/analyze")
def analyze_position(req: AnalyzeRequest):
    """
    Analyze a position and return best move
    """

    try:
        board, side = fen_to_bitboard(req.fen)

        if req.engine == "minimax":
            move, score = minimax_engine.find_best_move(
                board, req.depth, side
            )

        elif req.engine == "mcts":
            move = mcts_engine.search(board, side)
            score = None

        else:  # hybrid default
            move, score = hybrid_engine.find_best_move(
                board, req.depth, side
            )

        return {
            "best_move": move_to_uci(move) if move else None,
            "score": score,
            "engine": req.engine
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/evaluate")
def evaluate_position(req: AnalyzeRequest):
    """
    Return evaluation score only
    """

    try:
        board, side = fen_to_bitboard(req.fen)

        score = hybrid_engine.evaluate(board)

        return {
            "score": score
        }

    except Exception as e:
        return {"error": str(e)}