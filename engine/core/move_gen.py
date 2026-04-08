# move_gen.py
# High-performance move generator using bitboards

from bitboard import (
    WHITE, BLACK,
    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING,
    KNIGHT_MOVES, KING_MOVES, PAWN_ATTACKS,
    pop_lsb
)

# ===============================
# MOVE REPRESENTATION
# ===============================

class Move:
    def __init__(self, from_sq, to_sq, piece, capture=False, promotion=None):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.piece = piece
        self.capture = capture
        self.promotion = promotion

    def __repr__(self):
        return f"{self.from_sq}->{self.to_sq}"


# ===============================
# SLIDING DIRECTIONS
# ===============================

BISHOP_DIRS = [9, 7, -7, -9]
ROOK_DIRS = [8, -8, 1, -1]

# ===============================
# HELPER
# ===============================

def on_board(square):
    return 0 <= square < 64

def same_row(a, b):
    return (a // 8) == (b // 8)

# ===============================
# PAWN MOVES
# ===============================

def generate_pawn_moves(board, color):
    moves = []
    pawns = board.pieces[color][PAWN]
    enemy_occ = board.occupancy[1 - color]
    all_occ = board.all_occupancy

    direction = 8 if color == WHITE else -8
    start_rank = 1 if color == WHITE else 6
    promotion_rank = 6 if color == WHITE else 1

    bb = pawns
    while bb:
        sq, bb = pop_lsb(bb)

        # forward move
        forward = sq + direction
        if on_board(forward) and not (all_occ & (1 << forward)):
            # promotion
            if (sq // 8) == promotion_rank:
                moves.append(Move(sq, forward, PAWN, promotion=QUEEN))
            else:
                moves.append(Move(sq, forward, PAWN))

            # double push
            if (sq // 8) == start_rank:
                double = sq + 2 * direction
                if not (all_occ & (1 << double)):
                    moves.append(Move(sq, double, PAWN))

        # captures
        attacks = PAWN_ATTACKS[color][sq]
        targets = attacks & enemy_occ

        temp = targets
        while temp:
            to_sq, temp = pop_lsb(temp)
            if (sq // 8) == promotion_rank:
                moves.append(Move(sq, to_sq, PAWN, True, QUEEN))
            else:
                moves.append(Move(sq, to_sq, PAWN, True))

    return moves


# ===============================
# KNIGHT MOVES
# ===============================

def generate_knight_moves(board, color):
    moves = []
    knights = board.pieces[color][KNIGHT]
    own_occ = board.occupancy[color]
    enemy_occ = board.occupancy[1 - color]

    bb = knights
    while bb:
        sq, bb = pop_lsb(bb)
        targets = KNIGHT_MOVES[sq] & ~own_occ

        temp = targets
        while temp:
            to_sq, temp = pop_lsb(temp)
            capture = bool((1 << to_sq) & enemy_occ)
            moves.append(Move(sq, to_sq, KNIGHT, capture))

    return moves


# ===============================
# KING MOVES
# ===============================

def generate_king_moves(board, color):
    moves = []
    king_bb = board.pieces[color][KING]
    own_occ = board.occupancy[color]
    enemy_occ = board.occupancy[1 - color]

    if king_bb == 0:
        return moves

    sq = (king_bb & -king_bb).bit_length() - 1
    targets = KING_MOVES[sq] & ~own_occ

    temp = targets
    while temp:
        to_sq, temp = pop_lsb(temp)
        capture = bool((1 << to_sq) & enemy_occ)
        moves.append(Move(sq, to_sq, KING, capture))

    return moves


# ===============================
# SLIDING PIECES
# ===============================

def generate_sliding_moves(board, color, piece, directions):
    moves = []
    pieces = board.pieces[color][piece]
    own_occ = board.occupancy[color]
    enemy_occ = board.occupancy[1 - color]

    bb = pieces
    while bb:
        sq, bb = pop_lsb(bb)

        for d in directions:
            current = sq
            while True:
                next_sq = current + d

                if not on_board(next_sq):
                    break

                # tránh wrap ngang (file A -> H bug)
                if d == 1 and (next_sq % 8 == 0):
                    break
                if d == -1 and (current % 8 == 0):
                    break

                if (1 << next_sq) & own_occ:
                    break

                capture = bool((1 << next_sq) & enemy_occ)
                moves.append(Move(sq, next_sq, piece, capture))

                if capture:
                    break

                if (1 << next_sq) & board.all_occupancy:
                    break

                current = next_sq

    return moves


# ===============================
# MAIN GENERATOR
# ===============================

def generate_moves(board, color):
    moves = []

    moves += generate_pawn_moves(board, color)
    moves += generate_knight_moves(board, color)
    moves += generate_king_moves(board, color)

    moves += generate_sliding_moves(board, color, BISHOP, BISHOP_DIRS)
    moves += generate_sliding_moves(board, color, ROOK, ROOK_DIRS)
    moves += generate_sliding_moves(board, color, QUEEN, BISHOP_DIRS + ROOK_DIRS)

    return moves