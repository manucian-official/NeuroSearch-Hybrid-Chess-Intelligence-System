# zobrist.py
# Zobrist hashing for chess engine

import random

from bitboard import (
    WHITE, BLACK,
    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
)

# ===============================
# CONFIG
# ===============================

RANDOM_SEED = 2026
random.seed(RANDOM_SEED)

# ===============================
# ZOBRIST TABLES
# ===============================

# [color][piece][square]
ZOBRIST_PIECES = [[[0 for _ in range(64)] for _ in range(6)] for _ in range(2)]

# Castling rights (4 flags)
# WK, WQ, BK, BQ
ZOBRIST_CASTLING = [0] * 4

# En passant file (0–7)
ZOBRIST_ENPASSANT = [0] * 8

# Side to move
ZOBRIST_SIDE = 0

# ===============================
# INIT
# ===============================

def rand64():
    return random.getrandbits(64)

def init_zobrist():
    global ZOBRIST_SIDE

    # Pieces
    for color in (WHITE, BLACK):
        for piece in range(6):
            for sq in range(64):
                ZOBRIST_PIECES[color][piece][sq] = rand64()

    # Castling
    for i in range(4):
        ZOBRIST_CASTLING[i] = rand64()

    # En passant
    for i in range(8):
        ZOBRIST_ENPASSANT[i] = rand64()

    # Side
    ZOBRIST_SIDE = rand64()


# Initialize once
init_zobrist()


# ===============================
# HASH COMPUTATION
# ===============================

def compute_hash(board, side_to_move, castling_rights=0b1111, en_passant_file=None):
    """
    board: Bitboard object
    side_to_move: WHITE / BLACK
    castling_rights: 4-bit mask (WK WQ BK BQ)
    en_passant_file: 0–7 or None
    """

    h = 0

    # Pieces
    for color in (WHITE, BLACK):
        for piece in range(6):
            bb = board.pieces[color][piece]

            while bb:
                sq = (bb & -bb).bit_length() - 1
                bb &= bb - 1
                h ^= ZOBRIST_PIECES[color][piece][sq]

    # Castling
    for i in range(4):
        if castling_rights & (1 << i):
            h ^= ZOBRIST_CASTLING[i]

    # En passant
    if en_passant_file is not None:
        h ^= ZOBRIST_ENPASSANT[en_passant_file]

    # Side to move
    if side_to_move == BLACK:
        h ^= ZOBRIST_SIDE

    return h


# ===============================
# INCREMENTAL UPDATE (IMPORTANT)
# ===============================

def update_hash_piece(h, color, piece, square):
    """Toggle piece at square (add/remove)"""
    return h ^ ZOBRIST_PIECES[color][piece][square]


def update_hash_side(h):
    """Switch side to move"""
    return h ^ ZOBRIST_SIDE


def update_hash_castling(h, old_rights, new_rights):
    """Update castling rights"""
    for i in range(4):
        if (old_rights ^ new_rights) & (1 << i):
            h ^= ZOBRIST_CASTLING[i]
    return h


def update_hash_enpassant(h, old_file, new_file):
    """Update en passant file"""
    if old_file is not None:
        h ^= ZOBRIST_ENPASSANT[old_file]
    if new_file is not None:
        h ^= ZOBRIST_ENPASSANT[new_file]
    return h