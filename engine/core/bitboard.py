# bitboard.py
# High-performance bitboard implementation for chess engine

from dataclasses import dataclass

# ===============================
# CONSTANTS
# ===============================

WHITE, BLACK = 0, 1

PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = range(6)

FILES = "abcdefgh"
RANKS = "12345678"

# Precomputed masks
FILE_MASKS = [0] * 8
RANK_MASKS = [0] * 8

for file in range(8):
    for rank in range(8):
        sq = rank * 8 + file
        FILE_MASKS[file] |= (1 << sq)
        RANK_MASKS[rank] |= (1 << sq)

# ===============================
# HELPER FUNCTIONS
# ===============================

def bit_count(bb: int) -> int:
    return bb.bit_count()

def lsb(bb: int) -> int:
    """Get index of least significant bit"""
    return (bb & -bb).bit_length() - 1

def pop_lsb(bb: int) -> (int, int):
    """Pop least significant bit and return (index, new_bb)"""
    lsb_index = lsb(bb)
    bb &= bb - 1
    return lsb_index, bb

def square_to_coords(square: int):
    return (square % 8, square // 8)

def coords_to_square(file: int, rank: int):
    return rank * 8 + file

# ===============================
# BITBOARD CLASS
# ===============================

@dataclass
class Bitboard:
    pieces: list  # [color][piece_type] => bitboard

    def __init__(self):
        self.pieces = [[0]*6 for _ in range(2)]
        self.occupancy = [0, 0]
        self.all_occupancy = 0

    # ===============================
    # SETUP
    # ===============================

    def set_piece(self, color, piece, square):
        bb = 1 << square
        self.pieces[color][piece] |= bb
        self.occupancy[color] |= bb
        self.all_occupancy |= bb

    def remove_piece(self, color, piece, square):
        bb = ~(1 << square)
        self.pieces[color][piece] &= bb
        self.occupancy[color] &= bb
        self.all_occupancy &= bb

    def move_piece(self, color, piece, from_sq, to_sq):
        self.remove_piece(color, piece, from_sq)
        self.set_piece(color, piece, to_sq)

    # ===============================
    # QUERIES
    # ===============================

    def get_piece_at(self, square):
        mask = 1 << square
        for color in (WHITE, BLACK):
            for piece in range(6):
                if self.pieces[color][piece] & mask:
                    return color, piece
        return None

    def is_occupied(self, square):
        return bool(self.all_occupancy & (1 << square))

    def get_occupancy(self, color=None):
        if color is None:
            return self.all_occupancy
        return self.occupancy[color]

    # ===============================
    # DEBUG / VISUALIZATION
    # ===============================

    def print_board(self):
        piece_symbols = ["P", "N", "B", "R", "Q", "K"]

        board = ["." for _ in range(64)]

        for color in (WHITE, BLACK):
            for piece in range(6):
                bb = self.pieces[color][piece]
                while bb:
                    sq, bb = pop_lsb(bb)
                    symbol = piece_symbols[piece]
                    if color == BLACK:
                        symbol = symbol.lower()
                    board[sq] = symbol

        for rank in reversed(range(8)):
            row = board[rank*8:(rank+1)*8]
            print(" ".join(row))
        print()

# ===============================
# ATTACK TABLES (BASIC)
# ===============================

KNIGHT_MOVES = [0] * 64
KING_MOVES = [0] * 64

def init_leaper_attacks():
    for sq in range(64):
        file, rank = square_to_coords(sq)

        # Knight
        moves = [
            (file+1, rank+2), (file+2, rank+1),
            (file+2, rank-1), (file+1, rank-2),
            (file-1, rank-2), (file-2, rank-1),
            (file-2, rank+1), (file-1, rank+2)
        ]
        for f, r in moves:
            if 0 <= f < 8 and 0 <= r < 8:
                KNIGHT_MOVES[sq] |= (1 << coords_to_square(f, r))

        # King
        moves = [
            (file+1, rank), (file+1, rank+1),
            (file, rank+1), (file-1, rank+1),
            (file-1, rank), (file-1, rank-1),
            (file, rank-1), (file+1, rank-1)
        ]
        for f, r in moves:
            if 0 <= f < 8 and 0 <= r < 8:
                KING_MOVES[sq] |= (1 << coords_to_square(f, r))

init_leaper_attacks()

# ===============================
# PAWN ATTACKS
# ===============================

PAWN_ATTACKS = [[0]*64 for _ in range(2)]

def init_pawn_attacks():
    for sq in range(64):
        file, rank = square_to_coords(sq)

        # WHITE
        for f, r in [(file-1, rank+1), (file+1, rank+1)]:
            if 0 <= f < 8 and 0 <= r < 8:
                PAWN_ATTACKS[WHITE][sq] |= (1 << coords_to_square(f, r))

        # BLACK
        for f, r in [(file-1, rank-1), (file+1, rank-1)]:
            if 0 <= f < 8 and 0 <= r < 8:
                PAWN_ATTACKS[BLACK][sq] |= (1 << coords_to_square(f, r))

init_pawn_attacks()