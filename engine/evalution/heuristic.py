# heuristic.py
# Advanced evaluation function for chess engine

from bitboard import (
    WHITE, BLACK,
    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING,
    pop_lsb
)

# ===============================
# PIECE VALUES
# ===============================

PIECE_VALUES = {
    PAWN: 100,
    KNIGHT: 320,
    BISHOP: 330,
    ROOK: 500,
    QUEEN: 900,
    KING: 20000
}

# ===============================
# PIECE-SQUARE TABLES
# (simple version)
# ===============================

PAWN_TABLE = [
      0, 0, 0, 0, 0, 0, 0, 0,
     50,50,50,50,50,50,50,50,
     10,10,20,30,30,20,10,10,
      5, 5,10,25,25,10, 5, 5,
      0, 0, 0,20,20, 0, 0, 0,
      5,-5,-10, 0, 0,-10,-5, 5,
      5,10,10,-20,-20,10,10, 5,
      0, 0, 0, 0, 0, 0, 0, 0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

TABLES = {
    PAWN: PAWN_TABLE,
    KNIGHT: KNIGHT_TABLE
}

# ===============================
# CORE EVALUATION
# ===============================

def evaluate(board):
    """
    Positive score = WHITE advantage
    Negative score = BLACK advantage
    """

    score = 0

    score += material_score(board)
    score += piece_square_score(board)
    score += mobility_score(board)
    score += pawn_structure_score(board)
    score += king_safety_score(board)

    return score


# ===============================
# MATERIAL
# ===============================

def material_score(board):
    score = 0

    for color in (WHITE, BLACK):
        sign = 1 if color == WHITE else -1

        for piece in range(6):
            count = board.pieces[color][piece].bit_count()
            score += sign * PIECE_VALUES[piece] * count

    return score


# ===============================
# PIECE-SQUARE TABLE
# ===============================

def piece_square_score(board):
    score = 0

    for color in (WHITE, BLACK):
        sign = 1 if color == WHITE else -1

        for piece, table in TABLES.items():
            bb = board.pieces[color][piece]

            while bb:
                sq, bb = pop_lsb(bb)

                # mirror for black
                if color == BLACK:
                    sq = 63 - sq

                score += sign * table[sq]

    return score


# ===============================
# MOBILITY
# ===============================

def mobility_score(board):
    """
    Simple mobility: number of available moves (approx)
    """
    score = 0

    for color in (WHITE, BLACK):
        sign = 1 if color == WHITE else -1

        mobility = 0

        for piece in range(6):
            bb = board.pieces[color][piece]
            mobility += bb.bit_count()

        score += sign * mobility * 2

    return score


# ===============================
# PAWN STRUCTURE
# ===============================

def pawn_structure_score(board):
    score = 0

    for color in (WHITE, BLACK):
        sign = 1 if color == WHITE else -1
        pawns = board.pieces[color][PAWN]

        files = [0]*8

        bb = pawns
        while bb:
            sq, bb = pop_lsb(bb)
            file = sq % 8
            files[file] += 1

        for f in range(8):
            if files[f] > 1:
                score -= sign * 10  # doubled pawn

            if files[f] > 0:
                if (f == 0 or files[f-1] == 0) and (f == 7 or files[f+1] == 0):
                    score -= sign * 15  # isolated pawn

    return score


# ===============================
# KING SAFETY
# ===============================

def king_safety_score(board):
    score = 0

    for color in (WHITE, BLACK):
        sign = 1 if color == WHITE else -1
        king_bb = board.pieces[color][KING]

        if king_bb == 0:
            continue

        sq = (king_bb & -king_bb).bit_length() - 1
        rank = sq // 8

        # basic: king should stay back
        if color == WHITE:
            score += sign * (7 - rank) * 5
        else:
            score += sign * rank * 5

    return score