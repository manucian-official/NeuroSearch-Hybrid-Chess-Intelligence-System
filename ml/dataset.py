# minimax.py
# Minimax + Alpha-Beta + basic optimizations

from move_gen import generate_moves
from heuristic import evaluate
from zobrist import compute_hash

INF = 10**9

# ===============================
# TRANSPOSITION TABLE
# ===============================

TT = {}

class TTEntry:
    def __init__(self, depth, score):
        self.depth = depth
        self.score = score


# ===============================
# MINIMAX ENGINE
# ===============================

class MinimaxEngine:
    def __init__(self):
        self.nodes = 0

    # ===============================
    # MAIN SEARCH
    # ===============================

    def search(self, board, depth, alpha, beta, maximizing, side):
        self.nodes += 1

        # Zobrist hash
        h = compute_hash(board, side)

        # Transposition Table
        if h in TT:
            entry = TT[h]
            if entry.depth >= depth:
                return entry.score

        # Leaf node
        if depth == 0:
            return self.quiescence(board, alpha, beta, side)

        moves = generate_moves(board, side)

        if not moves:
            return evaluate(board)

        # Move ordering (captures first)
        moves.sort(key=lambda m: m.capture, reverse=True)

        if maximizing:
            value = -INF

            for move in moves:
                captured = self.make_move(board, move, side)

                score = self.search(
                    board, depth - 1, alpha, beta, False, 1 - side
                )

                self.undo_move(board, move, side, captured)

                value = max(value, score)
                alpha = max(alpha, score)

                if alpha >= beta:
                    break  # beta cutoff

            TT[h] = TTEntry(depth, value)
            return value

        else:
            value = INF

            for move in moves:
                captured = self.make_move(board, move, side)

                score = self.search(
                    board, depth - 1, alpha, beta, True, 1 - side
                )

                self.undo_move(board, move, side, captured)

                value = min(value, score)
                beta = min(beta, score)

                if alpha >= beta:
                    break  # alpha cutoff

            TT[h] = TTEntry(depth, value)
            return value

    # ===============================
    # QUIESCENCE SEARCH
    # ===============================

    def quiescence(self, board, alpha, beta, side):
        stand_pat = evaluate(board)

        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        moves = generate_moves(board, side)

        # only capture moves
        moves = [m for m in moves if m.capture]

        for move in moves:
            captured = self.make_move(board, move, side)

            score = -self.quiescence(board, -beta, -alpha, 1 - side)

            self.undo_move(board, move, side, captured)

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha

    # ===============================
    # MAKE / UNDO MOVE
    # ===============================

    def make_move(self, board, move, side):
        piece = move.piece
        captured_piece = None

        # capture
        if move.capture:
            target = board.get_piece_at(move.to_sq)
            if target:
                enemy_color, enemy_piece = target
                captured_piece = (enemy_color, enemy_piece)
                board.remove_piece(enemy_color, enemy_piece, move.to_sq)

        # move
        board.move_piece(side, piece, move.from_sq, move.to_sq)

        # promotion
        if move.promotion is not None:
            board.remove_piece(side, piece, move.to_sq)
            board.set_piece(side, move.promotion, move.to_sq)

        return captured_piece

    def undo_move(self, board, move, side, captured_piece):
        piece = move.piece

        # undo promotion
        if move.promotion is not None:
            board.remove_piece(side, move.promotion, move.to_sq)
            board.set_piece(side, piece, move.from_sq)
        else:
            board.move_piece(side, piece, move.to_sq, move.from_sq)

        # restore captured
        if captured_piece:
            color, piece_type = captured_piece
            board.set_piece(color, piece_type, move.to_sq)

    # ===============================
    # FIND BEST MOVE
    # ===============================

    def find_best_move(self, board, depth, side):
        best_move = None
        best_score = -INF

        moves = generate_moves(board, side)
        moves.sort(key=lambda m: m.capture, reverse=True)

        for move in moves:
            captured = self.make_move(board, move, side)

            score = self.search(
                board, depth - 1, -INF, INF, False, 1 - side
            )

            self.undo_move(board, move, side, captured)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move, best_score